"""
YouTube Data API v3 scraper.

Searches for educational videos per skill keyword and returns
structured course-like records for the knowledge RAG.

Uses the same Gemini API key (Google Cloud project).
"""

import hashlib
import logging
import re

import httpx

from app.config import settings
from app.scrapers.config import SKILL_TRACK_MAP, YOUTUBE_SEARCH_TERMS
from app.scrapers.normalizer import infer_level_from_text

logger = logging.getLogger(__name__)

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"


async def scrape_youtube_all(api_key: str, max_per_query: int = 5) -> list[dict]:
    """
    Search YouTube for educational videos across all skill keywords.

    Args:
        api_key: YouTube Data API v3 key
        max_per_query: Max results per search query (API quota optimization)

    Returns:
        List of structured course dicts
    """
    all_courses = []
    seen_ids = set()

    async with httpx.AsyncClient(timeout=15) as client:
        for skill, queries in YOUTUBE_SEARCH_TERMS.items():
            tracks = SKILL_TRACK_MAP.get(skill, ["backend_engineer"])

            for query in queries:
                try:
                    videos = await _search_videos(client, api_key, query, max_per_query)

                    for video in videos:
                        video_id = video.get("id", {}).get("videoId")
                        if not video_id or video_id in seen_ids:
                            continue
                        seen_ids.add(video_id)

                        course = _video_to_course(video, skill, tracks)
                        if course:
                            all_courses.append(course)

                except Exception as e:
                    logger.error(f"[YouTube] Error searching '{query}': {e}")

            logger.info(f"[YouTube] Skill '{skill}': done ({len(queries)} queries)")

    # Enrich with video details (duration, view count)
    if all_courses:
        video_ids = [c["external_id"] for c in all_courses if c.get("external_id")]
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                details = await _get_video_details(client, api_key, video_ids)
                _enrich_courses_with_details(all_courses, details)
        except Exception as e:
            logger.warning(f"[YouTube] Could not fetch video details: {e}")

    logger.info(f"[YouTube] Total: {len(all_courses)} videos scraped")
    return all_courses


async def _search_videos(
    client: httpx.AsyncClient,
    api_key: str,
    query: str,
    max_results: int,
) -> list[dict]:
    """Search YouTube for videos matching a query."""
    response = await client.get(
        YOUTUBE_SEARCH_URL,
        params={
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "order": "relevance",
            "videoDuration": "medium",  # 4-20 min — tutorial-length
            "relevanceLanguage": "id",  # Prefer Indonesian content
            "key": api_key,
        },
    )

    if response.status_code != 200:
        logger.warning(f"[YouTube] Search API returned {response.status_code}: {response.text[:200]}")
        return []

    data = response.json()
    return data.get("items", [])


async def _get_video_details(
    client: httpx.AsyncClient,
    api_key: str,
    video_ids: list[str],
) -> dict[str, dict]:
    """Fetch video details (duration, view count) for a batch of video IDs."""
    details = {}

    # YouTube API allows up to 50 IDs per request
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i : i + 50]
        response = await client.get(
            YOUTUBE_VIDEO_URL,
            params={
                "part": "contentDetails,statistics",
                "id": ",".join(batch),
                "key": api_key,
            },
        )

        if response.status_code != 200:
            continue

        for item in response.json().get("items", []):
            details[item["id"]] = {
                "duration": item.get("contentDetails", {}).get("duration"),
                "view_count": item.get("statistics", {}).get("viewCount"),
                "like_count": item.get("statistics", {}).get("likeCount"),
            }

    return details


def _video_to_course(video: dict, skill: str, tracks: list[str]) -> dict | None:
    """Convert a YouTube search result to a course dict."""
    snippet = video.get("snippet", {})
    video_id = video.get("id", {}).get("videoId")

    if not video_id or not snippet.get("title"):
        return None

    title = snippet["title"]
    channel = snippet.get("channelTitle", "Unknown")
    description = snippet.get("description", "")

    # Detect language from title/description
    is_indonesian = _is_indonesian(title + " " + description)
    language = "id" if is_indonesian else "en"

    # Infer level
    level = infer_level_from_text(title + " " + description)

    content_hash = hashlib.sha256(f"youtube:{video_id}".encode()).hexdigest()

    return {
        "source": "youtube",
        "external_id": video_id,
        "title": title,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "instructor": channel,
        "platform_display": "YouTube",
        "language": language,
        "level": level,
        "duration_hours": None,  # filled by _enrich_courses_with_details
        "price_idr_approx": 0,
        "is_free": True,
        "has_certificate": False,
        "rating": None,  # filled by _enrich_courses_with_details
        "rating_count": None,
        "skills_covered": [skill],
        "career_tracks": tracks,
        "description_short": description[:300] if description else None,
        "is_indonesia_specific": is_indonesian,
        "is_bahasa_indonesia": is_indonesian,
        "content_hash": content_hash,
        "topics_covered": [f"channel:{channel}", f"skill:{skill}"],
    }


def _enrich_courses_with_details(courses: list[dict], details: dict[str, dict]):
    """Add duration and view count from video details."""
    for course in courses:
        video_id = course.get("external_id")
        if video_id and video_id in details:
            info = details[video_id]

            # Parse ISO 8601 duration (PT1H23M45S → hours)
            duration = info.get("duration")
            if duration:
                course["duration_hours"] = _parse_iso_duration(duration)

            # View count as proxy for quality/popularity
            views = info.get("view_count")
            if views:
                course["rating_count"] = int(views)

            # Like count → synthetic rating (views with likes)
            likes = info.get("like_count")
            if likes and views and int(views) > 0:
                # Approximate quality score: like ratio scaled to 5.0
                ratio = int(likes) / int(views)
                course["rating"] = min(round(ratio * 100, 2), 5.0)


def _parse_iso_duration(duration: str) -> float | None:
    """Parse ISO 8601 duration (PT1H23M45S) to hours."""
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    if not match:
        return None
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return round(hours + minutes / 60 + seconds / 3600, 2)


def _is_indonesian(text: str) -> bool:
    """Simple heuristic to detect Indonesian language."""
    indonesian_words = [
        "belajar", "tutorial", "bahasa", "indonesia", "pemula",
        "dasar", "untuk", "cara", "lengkap", "mengenal",
        "membuat", "dengan", "menggunakan", "mudah", "kelas",
    ]
    text_lower = text.lower()
    matches = sum(1 for word in indonesian_words if word in text_lower)
    return matches >= 2
