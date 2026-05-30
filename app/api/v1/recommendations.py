"""
Course Recommendations — serve scraped courses based on user profile.

GET /recommendations/courses — Get recommended courses for user's target role
"""

import logging

from fastapi import APIRouter, Query

from app.api.deps import CurrentUser, DBSession
from app.db.models import Profile, Roadmap, ScrapedCourse
from app.schemas import APIResponse, RecommendationResponse
from sqlalchemy import func, or_, select

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/recommendations/courses", response_model=APIResponse)
async def get_course_recommendations(
    user: CurrentUser,
    db: DBSession,
    level: str | None = Query(default=None, description="Filter by level: beginner, intermediate, advanced"),
    source: str | None = Query(default=None, description="Filter by source: dicoding, youtube, rubythalib, book"),
    free_only: bool = Query(default=False, description="Only show free courses"),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=15, ge=1, le=50),
):
    """
    Get recommended courses from the scraped knowledge base.

    Matches courses against the user's target role career tracks.
    Falls back to returning popular courses if no profile exists.
    """
    offset = (page - 1) * per_page

    # Get user profile for targeting
    profile = await db.get(Profile, user.id)
    target_role = profile.target_role if profile else None

    # Build base query
    query = select(ScrapedCourse)
    count_query = select(func.count(ScrapedCourse.id))

    # Filter by career tracks matching target role
    if target_role:
        # Normalize target role for matching
        target_lower = target_role.lower().replace(" ", "_")
        # Match against career_tracks array or skills_covered
        track_filter = or_(
            ScrapedCourse.career_tracks.any(target_lower),
            ScrapedCourse.title.ilike(f"%{target_role}%"),
            ScrapedCourse.description_short.ilike(f"%{target_role}%"),
        )
        # Also try partial matches for common role keywords
        role_keywords = target_role.lower().split()
        for keyword in role_keywords:
            if len(keyword) > 3:  # skip short words
                track_filter = or_(
                    track_filter,
                    ScrapedCourse.career_tracks.any(keyword),
                    ScrapedCourse.skills_covered.any(keyword),
                )
        query = query.where(track_filter)
        count_query = count_query.where(track_filter)

    # Apply filters
    if level:
        query = query.where(ScrapedCourse.level == level)
        count_query = count_query.where(ScrapedCourse.level == level)

    if source:
        query = query.where(ScrapedCourse.source == source)
        count_query = count_query.where(ScrapedCourse.source == source)

    if free_only:
        query = query.where(ScrapedCourse.is_free == True)  # noqa: E712
        count_query = count_query.where(ScrapedCourse.is_free == True)  # noqa: E712

    # Get total count
    total = (await db.execute(count_query)).scalar()

    # If no results with career track filter, fall back to all courses
    if total == 0 and target_role:
        query = select(ScrapedCourse)
        count_query = select(func.count(ScrapedCourse.id))
        if level:
            query = query.where(ScrapedCourse.level == level)
            count_query = count_query.where(ScrapedCourse.level == level)
        if source:
            query = query.where(ScrapedCourse.source == source)
            count_query = count_query.where(ScrapedCourse.source == source)
        if free_only:
            query = query.where(ScrapedCourse.is_free == True)  # noqa: E712
            count_query = count_query.where(ScrapedCourse.is_free == True)  # noqa: E712
        total = (await db.execute(count_query)).scalar()

    # Order by rating (highest first), then by most recent
    result = await db.execute(
        query
        .order_by(
            ScrapedCourse.rating.desc().nullslast(),
            ScrapedCourse.created_at.desc(),
        )
        .offset(offset)
        .limit(per_page)
    )
    courses = result.scalars().all()

    return APIResponse(
        data={
            "items": [
                RecommendationResponse.model_validate(c).model_dump(mode="json")
                for c in courses
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
            "target_role": target_role,
        }
    )


@router.get("/recommendations/courses/by-roadmap", response_model=APIResponse)
async def get_recommendations_by_roadmap(
    user: CurrentUser,
    db: DBSession,
    phase: int | None = Query(default=None, description="Filter to a specific phase number"),
):
    """
    Get recommended courses grouped by roadmap phases.
    Maps scraped courses to milestones via skill matching.
    """
    # 1. Get user's active roadmap
    result = await db.execute(
        select(Roadmap).where(Roadmap.user_id == user.id, Roadmap.is_active == True)
    )
    roadmap = result.scalar_one_or_none()
    if not roadmap or not roadmap.roadmap_json:
        return APIResponse(data={"phases": []}, message="No active roadmap")

    phases_data = roadmap.roadmap_json.get("phases", [])

    # 2. Fetch all scraped courses
    all_courses_result = await db.execute(
        select(ScrapedCourse)
        .order_by(ScrapedCourse.rating.desc().nullslast())
        .limit(200)
    )
    all_courses = all_courses_result.scalars().all()

    # 3. Build skill → milestone/phase mapping
    grouped_phases = []
    used_course_ids = set()

    for p in phases_data:
        p_num = p.get("phase_number", 0)
        if phase is not None and p_num != phase:
            continue

        phase_milestones = []
        for ms in p.get("milestones", []):
            ms_skills = {s.lower() for s in (ms.get("skills") or [])}
            ms_title_words = {w.lower() for w in ms.get("title", "").split() if len(w) > 3}
            match_terms = ms_skills | ms_title_words

            matched = []
            for sc in all_courses:
                if sc.id in used_course_ids:
                    continue
                sc_skills = {s.lower() for s in (sc.skills_covered or [])}
                sc_title_words = {w.lower() for w in (sc.title or "").split() if len(w) > 3}
                sc_topics = {t.lower() for t in (sc.topics_covered or [])}
                sc_terms = sc_skills | sc_title_words | sc_topics

                overlap = match_terms & sc_terms
                if overlap:
                    matched.append((sc, len(overlap)))

            # Sort by match strength, take top 5 per milestone
            matched.sort(key=lambda x: x[1], reverse=True)
            ms_courses = []
            for sc, _ in matched[:5]:
                used_course_ids.add(sc.id)
                ms_courses.append(
                    RecommendationResponse.model_validate(sc).model_dump(mode="json")
                )

            phase_milestones.append({
                "milestone_id": ms.get("milestone_id"),
                "title": ms.get("title"),
                "skills": ms.get("skills", []),
                "courses": ms_courses,
            })

        grouped_phases.append({
            "phase_number": p_num,
            "phase_title": p.get("phase_title"),
            "description": p.get("description"),
            "milestones": phase_milestones,
        })

    return APIResponse(data={"phases": grouped_phases})
