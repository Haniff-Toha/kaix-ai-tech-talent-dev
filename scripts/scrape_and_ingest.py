"""
Master scrape & ingest script.

Runs all scrapers (Dicoding, YouTube, rubythalib, curated books),
stores results in scraped_courses, then generates RAG chunks
and embeds them into knowledge_rag.

Usage:
    python -m scripts.scrape_and_ingest
    python -m scripts.scrape_and_ingest --skip-dicoding
    python -m scripts.scrape_and_ingest --skip-youtube
"""

import argparse
import asyncio
import hashlib
import json
import logging
import sys

from app.config import settings
from app.db.session import async_session
from app.scrapers.dicoding import scrape_dicoding_all
from app.scrapers.youtube import scrape_youtube_all
from app.scrapers.rubythalib import get_rubythalib_courses, get_curated_books
from app.scrapers.rag_updater import update_course_rag
from sqlalchemy import text

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


async def store_courses(courses: list[dict]) -> int:
    """
    Upsert courses into scraped_courses table.
    Uses content_hash for deduplication.
    Returns count of stored records.
    """
    if not courses:
        return 0

    count = 0
    async with async_session() as db:
        for course in courses:
            content_hash = course.get("content_hash")
            if not content_hash:
                continue

            # Check if exists
            result = await db.execute(
                text("SELECT id FROM scraped_courses WHERE content_hash = :hash"),
                {"hash": content_hash},
            )
            existing = result.fetchone()

            if existing:
                # Update existing
                await db.execute(
                    text("""
                        UPDATE scraped_courses SET
                            title = :title,
                            url = :url,
                            instructor = :instructor,
                            platform_display = :platform_display,
                            language = :language,
                            level = :level,
                            duration_hours = :duration_hours,
                            price_idr_approx = :price_idr_approx,
                            is_free = :is_free,
                            has_certificate = :has_certificate,
                            rating = :rating,
                            rating_count = :rating_count,
                            skills_covered = :skills_covered,
                            career_tracks = :career_tracks,
                            description_short = :description_short,
                            topics_covered = :topics_covered,
                            is_indonesia_specific = :is_indonesia_specific,
                            is_bahasa_indonesia = :is_bahasa_indonesia,
                            last_scraped_at = now(),
                            updated_at = now()
                        WHERE content_hash = :content_hash
                    """),
                    _course_to_params(course),
                )
            else:
                # Insert new
                await db.execute(
                    text("""
                        INSERT INTO scraped_courses (
                            id, source, external_id, title, url, instructor,
                            platform_display, language, level, duration_hours,
                            price_idr_approx, is_free, has_certificate, rating,
                            rating_count, skills_covered, career_tracks,
                            description_short, topics_covered,
                            is_indonesia_specific, is_bahasa_indonesia,
                            content_hash
                        ) VALUES (
                            gen_random_uuid(), :source, :external_id, :title, :url, :instructor,
                            :platform_display, :language, :level, :duration_hours,
                            :price_idr_approx, :is_free, :has_certificate, :rating,
                            :rating_count, :skills_covered, :career_tracks,
                            :description_short, :topics_covered,
                            :is_indonesia_specific, :is_bahasa_indonesia,
                            :content_hash
                        )
                    """),
                    _course_to_params(course),
                )

            count += 1

        await db.commit()

    logger.info(f"Stored {count} courses in scraped_courses table")
    return count


def _course_to_params(course: dict) -> dict:
    """Convert course dict to SQL parameter dict."""
    return {
        "source": course.get("source", "unknown"),
        "external_id": course.get("external_id"),
        "title": course.get("title", ""),
        "url": course.get("url"),
        "instructor": course.get("instructor"),
        "platform_display": course.get("platform_display"),
        "language": course.get("language"),
        "level": course.get("level"),
        "duration_hours": course.get("duration_hours"),
        "price_idr_approx": course.get("price_idr_approx"),
        "is_free": course.get("is_free", False),
        "has_certificate": course.get("has_certificate"),
        "rating": course.get("rating"),
        "rating_count": course.get("rating_count"),
        "skills_covered": course.get("skills_covered") or [],
        "career_tracks": course.get("career_tracks") or [],
        "description_short": course.get("description_short"),
        "topics_covered": course.get("topics_covered") or [],
        "is_indonesia_specific": course.get("is_indonesia_specific", False),
        "is_bahasa_indonesia": course.get("is_bahasa_indonesia", False),
        "content_hash": course.get("content_hash"),
    }


async def main(skip_dicoding: bool = False, skip_youtube: bool = False):
    """Main ingestion pipeline."""
    all_courses = []

    # 1. Dicoding scraper
    if not skip_dicoding:
        logger.info("=" * 60)
        logger.info("PHASE 1: Scraping Dicoding learning paths...")
        logger.info("=" * 60)
        try:
            dicoding_courses = await scrape_dicoding_all()
            all_courses.extend(dicoding_courses)
            logger.info(f"Dicoding: {len(dicoding_courses)} courses scraped")
        except Exception as e:
            logger.error(f"Dicoding scraper failed: {e}")
    else:
        logger.info("Skipping Dicoding scraper")

    # 2. YouTube scraper
    if not skip_youtube:
        logger.info("=" * 60)
        logger.info("PHASE 2: Searching YouTube for educational videos...")
        logger.info("=" * 60)

        youtube_api_key = getattr(settings, "youtube_api_key", None) or settings.gemini_api_key
        try:
            youtube_courses = await scrape_youtube_all(
                api_key=youtube_api_key,
                max_per_query=3,  # 3 results per query to stay within quota
            )
            all_courses.extend(youtube_courses)
            logger.info(f"YouTube: {len(youtube_courses)} videos scraped")
        except Exception as e:
            logger.error(f"YouTube scraper failed: {e}")
    else:
        logger.info("Skipping YouTube scraper")

    # 3. rubythalib.ai (static)
    logger.info("=" * 60)
    logger.info("PHASE 3: Loading rubythalib.ai curated courses...")
    logger.info("=" * 60)
    rubythalib_courses = get_rubythalib_courses()
    all_courses.extend(rubythalib_courses)

    # 4. Curated books (static)
    logger.info("=" * 60)
    logger.info("PHASE 4: Loading curated books...")
    logger.info("=" * 60)
    book_courses = get_curated_books()
    all_courses.extend(book_courses)

    # 5. Store all courses in scraped_courses table
    logger.info("=" * 60)
    logger.info(f"PHASE 5: Storing {len(all_courses)} courses in DB...")
    logger.info("=" * 60)
    stored = await store_courses(all_courses)

    # 6. Generate RAG chunks and embed
    logger.info("=" * 60)
    logger.info(f"PHASE 6: Generating & embedding RAG chunks...")
    logger.info("=" * 60)
    rag_count = await update_course_rag(all_courses)

    # Summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("✅ INGESTION COMPLETE")
    logger.info("=" * 60)
    logger.info(f"  Courses stored: {stored}")
    logger.info(f"  RAG chunks added: {rag_count}")
    logger.info(f"  Sources: {', '.join(set(c.get('source', '?') for c in all_courses))}")
    logger.info("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape courses and ingest into Knowledge RAG")
    parser.add_argument("--skip-dicoding", action="store_true", help="Skip Dicoding scraper")
    parser.add_argument("--skip-youtube", action="store_true", help="Skip YouTube scraper")
    args = parser.parse_args()

    asyncio.run(main(skip_dicoding=args.skip_dicoding, skip_youtube=args.skip_youtube))
