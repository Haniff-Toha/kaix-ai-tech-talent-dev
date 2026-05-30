"""
Dicoding learning path scraper.

Scrapes all Dicoding learning paths (12 paths) + catalog fallback.
Extracts course data with sequence position for ordered curriculum info.
"""

import asyncio
import hashlib
import logging
import random
import re

import httpx
from bs4 import BeautifulSoup

from app.scrapers.config import (
    DICODING_CATALOG_URL,
    DICODING_LEARNING_PATHS,
    RATE_LIMIT_DELAY_SECONDS,
    random_user_agent,
)
from app.scrapers.normalizer import infer_level_from_text, infer_skills_from_text

logger = logging.getLogger(__name__)


async def scrape_dicoding_all() -> list[dict]:
    """
    Main entry point. Scrapes all Dicoding learning paths + catalog fallback.
    Returns list of structured course dicts.
    """
    all_courses = []

    async with httpx.AsyncClient(
        headers={"User-Agent": random_user_agent()},
        timeout=20,
        follow_redirects=True,
    ) as client:

        # 1. Scrape each learning path (ordered curriculum)
        for path_id, path_config in DICODING_LEARNING_PATHS.items():
            try:
                courses = await scrape_learning_path(client, path_id, path_config)
                all_courses.extend(courses)
                logger.info(
                    f"[Dicoding] Path '{path_config['name']}': {len(courses)} courses"
                )
                await asyncio.sleep(random.uniform(*RATE_LIMIT_DELAY_SECONDS))
            except Exception as e:
                logger.error(f"[Dicoding] Error scraping path {path_id}: {e}")

        # 2. Scrape catalog for uncovered courses
        try:
            catalog_courses = await scrape_dicoding_catalog(
                client, existing_ids={c.get("external_id") for c in all_courses}
            )
            all_courses.extend(catalog_courses)
            logger.info(f"[Dicoding] Catalog: {len(catalog_courses)} additional courses")
        except Exception as e:
            logger.error(f"[Dicoding] Error scraping catalog: {e}")

    logger.info(f"[Dicoding] Total: {len(all_courses)} courses scraped")
    return all_courses


async def scrape_learning_path(
    client: httpx.AsyncClient,
    path_id: int,
    path_config: dict,
) -> list[dict]:
    """Scrape a single Dicoding learning path page."""
    response = await client.get(path_config["url"])
    if response.status_code != 200:
        logger.warning(f"[Dicoding] Path {path_id} returned {response.status_code}")
        return []

    return parse_learning_path_page(
        html=response.text,
        path_id=path_id,
        path_name=path_config["name"],
        kaix_track=path_config["kaix_track"],
    )


def parse_learning_path_page(
    html: str,
    path_id: int,
    path_name: str,
    kaix_track: str,
) -> list[dict]:
    """Parse a Dicoding learning path page into course dicts."""
    soup = BeautifulSoup(html, "lxml")
    courses = []

    # Try multiple selectors for course cards
    course_cards = soup.select(
        ".course-item, "
        "[class*='CourseCard'], "
        "[class*='course-card'], "
        "article[class*='card']"
    )

    # Fallback: anchor tags linking to /academies/
    if not course_cards:
        course_cards = soup.find_all("a", href=re.compile(r"/academies/\d+"))

    for sequence, card in enumerate(course_cards, start=1):
        try:
            course = extract_course_from_card(
                card=card,
                kaix_track=kaix_track,
                path_id=path_id,
                path_name=path_name,
                sequence=sequence,
            )
            if course:
                courses.append(course)
        except Exception as e:
            logger.debug(f"[Dicoding] Card parse error (path {path_id}, seq {sequence}): {e}")

    return courses


def extract_course_from_card(
    card,
    kaix_track: str,
    path_id: int | None,
    path_name: str,
    sequence: int,
) -> dict | None:
    """Extract structured course data from a single Dicoding course card."""
    # Title
    title_el = (
        card.select_one("h3") or
        card.select_one("h4") or
        card.select_one("[class*='title']") or
        card.select_one("strong")
    )
    if not title_el:
        return None
    title = title_el.get_text(strip=True)
    if not title or len(title) < 5:
        return None

    # URL
    link_el = card if card.name == "a" else card.select_one("a[href*='/academies/']")
    url = None
    academy_id = None
    if link_el and link_el.get("href"):
        href = link_el["href"]
        if not href.startswith("http"):
            href = f"https://www.dicoding.com{href}"
        url = href
        id_match = re.search(r"/academies/(\d+)", href)
        if id_match:
            academy_id = id_match.group(1)

    # Level
    level_el = card.select_one("[class*='level'], [class*='difficulty'], [class*='tingkat'], [class*='badge']")
    level_text = level_el.get_text(strip=True).lower() if level_el else ""
    level = _parse_dicoding_level(level_text or title)

    # Duration
    duration_el = card.select_one("[class*='duration'], [class*='jam'], [class*='hour']")
    duration_text = duration_el.get_text(strip=True) if duration_el else ""
    if not duration_text:
        card_text = card.get_text(" ", strip=True)
        dur_match = re.search(r"(\d+)\s*[Jj]am", card_text)
        if dur_match:
            duration_text = f"{dur_match.group(1)} jam"
    duration_hours = _parse_duration(duration_text)

    # Rating
    rating_el = card.select_one("[class*='rating'], [class*='star']")
    rating_text = rating_el.get_text(strip=True) if rating_el else ""
    rating = _parse_rating(rating_text)

    # Enrollment
    enrollment_el = card.select_one("[class*='student'], [class*='siswa'], [class*='enrolled']")
    enrollment_text = enrollment_el.get_text(strip=True) if enrollment_el else ""
    enrollment = _parse_enrollment(enrollment_text)

    # Price
    price_el = card.select_one("[class*='price'], [class*='harga']")
    price_text = price_el.get_text(strip=True) if price_el else ""
    is_free, price_idr = _parse_dicoding_price(price_text, card.get_text(" ", strip=True))

    # Certificate
    has_cert_el = card.select_one("[class*='cert'], [class*='sertifikat']")
    has_certificate = has_cert_el is not None or not is_free

    # Skills
    skills = infer_skills_from_text(title)

    # Module count
    mod_match = re.search(r"(\d+)\s*[Mm]odul", card.get_text())
    module_count = int(mod_match.group(1)) if mod_match else None

    content_hash = hashlib.sha256(f"dicoding:{academy_id or title}".encode()).hexdigest()

    return {
        "source": "dicoding",
        "external_id": academy_id or title,
        "title": title,
        "url": url,
        "instructor": None,
        "platform_display": "Dicoding",
        "language": "id",
        "level": level,
        "duration_hours": duration_hours,
        "price_idr_approx": price_idr,
        "is_free": is_free,
        "has_certificate": has_certificate,
        "rating": rating,
        "rating_count": enrollment,
        "skills_covered": skills,
        "career_tracks": [kaix_track],
        "description_short": None,
        "is_indonesia_specific": True,
        "is_bahasa_indonesia": True,
        "content_hash": content_hash,
        "topics_covered": [
            f"dicoding_path_id:{path_id}" if path_id else "",
            f"dicoding_path_name:{path_name}",
            f"dicoding_path_sequence:{sequence}",
            f"module_count:{module_count}" if module_count else "",
        ],
    }


async def scrape_dicoding_catalog(
    client: httpx.AsyncClient,
    existing_ids: set[str],
) -> list[dict]:
    """Scrape catalog page for courses not in any learning path."""
    response = await client.get(DICODING_CATALOG_URL)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "lxml")
    courses = []
    seen_ids = set()

    academy_links = soup.find_all("a", href=re.compile(r"/academies/\d+"))

    for link in academy_links:
        href = link.get("href", "")
        id_match = re.search(r"/academies/(\d+)", href)
        if not id_match:
            continue

        academy_id = id_match.group(1)
        if academy_id in seen_ids or academy_id in existing_ids:
            continue
        seen_ids.add(academy_id)

        card = link.find_parent("article") or link.find_parent("div") or link
        course = extract_course_from_card(
            card=card,
            kaix_track=_infer_track_from_card(card),
            path_id=None,
            path_name="catalog",
            sequence=0,
        )
        if course:
            courses.append(course)

    return courses


# ── Private helpers ──────────────────────────────────────────────────

def _parse_dicoding_level(text: str) -> str:
    text = text.lower()
    if any(x in text for x in ["dasar", "pemula", "beginner", "basic"]):
        return "beginner"
    if any(x in text for x in ["menengah", "intermediate"]):
        return "intermediate"
    if any(x in text for x in ["mahir", "advanced", "expert", "profesional"]):
        return "advanced"
    return "beginner"


def _parse_dicoding_price(price_text: str, full_card_text: str) -> tuple[bool, int | None]:
    combined = (price_text + " " + full_card_text).lower()
    if any(x in combined for x in ["gratis", "free", "rp0", "rp 0"]):
        return True, 0
    return False, 150_000  # Dicoding subscription amortized


def _parse_enrollment(text: str) -> int | None:
    text = text.replace(".", "").replace(",", "")
    match = re.search(r"(\d+)", text)
    return int(match.group(1)) if match else None


def _parse_duration(text: str) -> float | None:
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:jam|hour|h)", text, re.IGNORECASE)
    return float(match.group(1)) if match else None


def _parse_rating(text: str) -> float | None:
    match = re.search(r"(\d+(?:\.\d+)?)", text)
    if match:
        val = float(match.group(1))
        return val if 0 <= val <= 5 else None
    return None


def _infer_track_from_card(card) -> str:
    text = card.get_text(" ", strip=True).lower()
    if any(x in text for x in ["back-end", "backend", "python server", "node.js server"]):
        return "backend_engineer"
    if any(x in text for x in ["front-end", "frontend", "react", "vue", "web"]):
        return "frontend_engineer"
    if any(x in text for x in ["devops", "cloud", "aws", "google cloud", "docker", "kubernetes"]):
        return "devops_engineer"
    if any(x in text for x in ["machine learning", "deep learning", "ai engineer", "data science"]):
        return "ml_ai_engineer"
    if any(x in text for x in ["data analyst", "analisis data"]):
        return "data_analyst"
    if any(x in text for x in ["android", "ios", "flutter", "mobile"]):
        return "frontend_engineer"
    if any(x in text for x in ["cyber", "security", "keamanan"]):
        return "cybersecurity_analyst"
    return "backend_engineer"
