"""
rubythalib.ai — Static course ingestion.

These courses are manually curated (not scraped) because
rubythalib.ai is a login-walled LMS with client-side rendering.
Updated quarterly.
"""

import hashlib
import logging

from app.scrapers.config import RUBYTHALIB_CURATED_COURSES, CURATED_BOOKS

logger = logging.getLogger(__name__)


def get_rubythalib_courses() -> list[dict]:
    """
    Return rubythalib.ai curated courses as structured dicts
    matching the scraped_courses schema.
    """
    courses = []

    for course_data in RUBYTHALIB_CURATED_COURSES:
        course = {**course_data}
        course["content_hash"] = hashlib.sha256(
            f"rubythalib:{course['title']}".encode()
        ).hexdigest()
        course.setdefault("external_id", course["title"])
        course.setdefault("duration_hours", None)
        course.setdefault("price_idr_approx", None)
        course.setdefault("rating", None)
        course.setdefault("rating_count", None)
        courses.append(course)

    logger.info(f"[rubythalib] Loaded {len(courses)} curated courses")
    return courses


def get_curated_books() -> list[dict]:
    """
    Return curated books as structured dicts.
    """
    courses = []

    for book_data in CURATED_BOOKS:
        course = {**book_data}
        course["content_hash"] = hashlib.sha256(
            f"book:{course['title']}".encode()
        ).hexdigest()
        course.setdefault("external_id", course["title"])
        course.setdefault("url", None)
        course.setdefault("duration_hours", None)
        course.setdefault("price_idr_approx", None)
        course.setdefault("rating", None)
        course.setdefault("rating_count", None)
        course.setdefault("is_indonesia_specific", False)
        course.setdefault("is_bahasa_indonesia", False)
        course.setdefault("has_certificate", False)
        course.setdefault("topics_covered", [])
        courses.append(course)

    logger.info(f"[Books] Loaded {len(courses)} curated books")
    return courses
