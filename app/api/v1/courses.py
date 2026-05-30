"""
Learning Hub — Courses CRUD + Study Sessions + Focus.

POST   /courses                    — Add a course
GET    /courses                    — List user's courses
PATCH  /courses/{id}               — Update course
DELETE /courses/{id}               — Remove course
POST   /courses/{id}/sessions      — Log a study session
GET    /courses/{id}/sessions      — Get session history
GET    /courses/today-focus        — Get today's focus courses
PATCH  /courses/{id}/toggle-focus  — Toggle focus for a course
GET    /courses/stats              — Get course stats (skills, platforms, activity)
"""

import logging
import uuid

from fastapi import APIRouter, Query

from app.agents.logging_classifier import run_logging_classifier
from app.api.deps import CurrentUser, DBSession
from app.db.models import Course, CourseSession
from app.schemas import (
    APIResponse,
    CourseRequest,
    CourseResponse,
    CourseSessionRequest,
    CourseSessionResponse,
    CourseUpdateRequest,
)
from app.services.streak_service import streak_service
from sqlalchemy import func, select

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/courses", response_model=APIResponse)
async def add_course(
    request: CourseRequest,
    user: CurrentUser,
    db: DBSession,
):
    """Add a learning source (book, course, video series, etc.)."""
    course = Course(
        user_id=user.id,
        title=request.title,
        platform=request.platform,
        url=request.url,
        linked_milestone_id=request.linked_milestone_id,
        estimated_hours=request.estimated_hours,
        status="not_started",
    )
    db.add(course)
    await db.flush()

    return APIResponse(
        data=CourseResponse.model_validate(course).model_dump(mode="json"),
        message="Kursus ditambahkan! / Course added!",
    )


@router.get("/courses", response_model=APIResponse)
async def list_courses(
    user: CurrentUser,
    db: DBSession,
    status: str | None = Query(default=None, pattern="^(not_started|in_progress|completed)$"),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=50),
):
    """Get user's courses with optional status filter."""
    offset = (page - 1) * per_page

    query = select(Course).where(Course.user_id == user.id)
    count_query = select(func.count(Course.id)).where(Course.user_id == user.id)

    if status:
        query = query.where(Course.status == status)
        count_query = count_query.where(Course.status == status)

    # Total count
    total = (await db.execute(count_query)).scalar()

    # Fetch
    result = await db.execute(
        query.order_by(Course.updated_at.desc()).offset(offset).limit(per_page)
    )
    courses = result.scalars().all()

    return APIResponse(
        data={
            "items": [
                CourseResponse.model_validate(c).model_dump(mode="json")
                for c in courses
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
        }
    )


@router.patch("/courses/{course_id}", response_model=APIResponse)
async def update_course(
    course_id: uuid.UUID,
    request: CourseUpdateRequest,
    user: CurrentUser,
    db: DBSession,
):
    """Update course metadata or status."""
    course = await db.get(Course, course_id)
    if not course or course.user_id != user.id:
        return APIResponse(
            success=False,
            message="Kursus tidak ditemukan / Course not found",
        )

    # Apply partial updates
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)

    await db.flush()

    return APIResponse(
        data=CourseResponse.model_validate(course).model_dump(mode="json"),
        message="Kursus diperbarui / Course updated",
    )


@router.delete("/courses/{course_id}", response_model=APIResponse)
async def delete_course(
    course_id: uuid.UUID,
    user: CurrentUser,
    db: DBSession,
):
    """Remove a course."""
    course = await db.get(Course, course_id)
    if not course or course.user_id != user.id:
        return APIResponse(
            success=False,
            message="Kursus tidak ditemukan / Course not found",
        )

    await db.delete(course)
    await db.flush()
    return APIResponse(message="Kursus dihapus / Course deleted")


@router.post("/courses/{course_id}/sessions", response_model=APIResponse)
async def log_course_session(
    course_id: uuid.UUID,
    request: CourseSessionRequest,
    user: CurrentUser,
    db: DBSession,
):
    """
    Log a study session for a course.

    Side effects:
        - Updates course completed_hours
        - Updates course status to in_progress if was not_started
        - Triggers Logging Classifier to map against roadmap
        - Updates streak
    """
    course = await db.get(Course, course_id)
    if not course or course.user_id != user.id:
        return APIResponse(
            success=False,
            message="Kursus tidak ditemukan / Course not found",
        )

    # Create session
    session = CourseSession(
        course_id=course_id,
        user_id=user.id,
        duration_minutes=request.duration_minutes,
        notes=request.notes,
    )
    db.add(session)

    # Update course hours
    hours_added = request.duration_minutes / 60
    course.completed_hours = (course.completed_hours or 0) + hours_added

    # Auto-update status
    if course.status == "not_started":
        course.status = "in_progress"
    if course.estimated_hours and course.completed_hours >= course.estimated_hours:
        course.status = "completed"

    await db.flush()
    await db.refresh(course)

    # Auto-classify this session as an activity against the roadmap
    activity_text = f"Belajar '{course.title}'"
    if course.platform:
        activity_text += f" di {course.platform}"
    if request.notes:
        activity_text += f": {request.notes}"

    classification = None
    try:
        classification = await run_logging_classifier(
            db=db,
            user=user,
            raw_text=activity_text,
            duration_minutes=request.duration_minutes,
        )
    except Exception as e:
        logger.warning(f"Auto-classification failed for course session: {e}")
        # Still update streak even if classification fails
        await streak_service.update_streak(db, user.id)

    return APIResponse(
        data={
            "session": CourseSessionResponse.model_validate(session).model_dump(mode="json"),
            "course": CourseResponse.model_validate(course).model_dump(mode="json"),
            "classification": classification,
        },
        message="Sesi belajar dicatat! / Study session logged!",
    )


@router.get("/courses/{course_id}/sessions", response_model=APIResponse)
async def list_course_sessions(
    course_id: uuid.UUID,
    user: CurrentUser,
    db: DBSession,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=50),
):
    """Get session history for a course."""
    course = await db.get(Course, course_id)
    if not course or course.user_id != user.id:
        return APIResponse(
            success=False,
            message="Kursus tidak ditemukan / Course not found",
        )

    offset = (page - 1) * per_page

    count_result = await db.execute(
        select(func.count(CourseSession.id)).where(CourseSession.course_id == course_id)
    )
    total = count_result.scalar()

    result = await db.execute(
        select(CourseSession)
        .where(CourseSession.course_id == course_id)
        .order_by(CourseSession.logged_at.desc())
        .offset(offset)
        .limit(per_page)
    )
    sessions = result.scalars().all()

    return APIResponse(
        data={
            "items": [
                CourseSessionResponse.model_validate(s).model_dump(mode="json")
                for s in sessions
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
            "course": CourseResponse.model_validate(course).model_dump(mode="json"),
        }
    )


@router.get("/courses/today-focus", response_model=APIResponse)
async def get_today_focus(user: CurrentUser, db: DBSession):
    """Get courses marked as today's focus."""
    result = await db.execute(
        select(Course)
        .where(Course.user_id == user.id, Course.is_today_focus == True)  # noqa: E712
        .order_by(Course.updated_at.desc())
    )
    courses = result.scalars().all()

    return APIResponse(
        data={
            "items": [
                CourseResponse.model_validate(c).model_dump(mode="json")
                for c in courses
            ],
        }
    )


@router.patch("/courses/{course_id}/toggle-focus", response_model=APIResponse)
async def toggle_course_focus(
    course_id: uuid.UUID,
    user: CurrentUser,
    db: DBSession,
):
    """Toggle is_today_focus on a course."""
    course = await db.get(Course, course_id)
    if not course or course.user_id != user.id:
        return APIResponse(
            success=False,
            message="Kursus tidak ditemukan / Course not found",
        )

    course.is_today_focus = not course.is_today_focus
    await db.flush()
    await db.refresh(course)

    return APIResponse(
        data=CourseResponse.model_validate(course).model_dump(mode="json"),
        message=f"Fokus {'aktif' if course.is_today_focus else 'nonaktif'}",
    )


@router.get("/courses/stats", response_model=APIResponse)
async def get_course_stats(user: CurrentUser, db: DBSession):
    """
    Get course statistics: skill mastery and platform distribution.

    Skill mastery is calculated per roadmap milestone:
    1. Sum completed_hours from all courses linked to a milestone
    2. Target hours from roadmap daily_tasks estimated_minutes, or 30h fallback
    3. pct = min(completed_hours / target_hours * 100, 100)
    """
    from datetime import datetime, timedelta
    from app.db.models import CourseSession, Roadmap

    DEFAULT_MILESTONE_HOURS = 30  # Fallback if no estimate available

    # Get all user courses
    result = await db.execute(
        select(Course).where(Course.user_id == user.id)
    )
    courses = result.scalars().all()

    # Platform distribution
    platform_counts: dict[str, int] = {}
    total_courses = len(courses)
    for c in courses:
        p = (c.platform or "Lainnya").capitalize()
        platform_counts[p] = platform_counts.get(p, 0) + 1

    platforms = [
        {"name": name, "count": count, "pct": round(count / total_courses * 100) if total_courses else 0}
        for name, count in sorted(platform_counts.items(), key=lambda x: -x[1])
    ]

    # Get active roadmap for milestone info
    roadmap_result = await db.execute(
        select(Roadmap)
        .where(Roadmap.user_id == user.id, Roadmap.is_active == True)  # noqa: E712
        .order_by(Roadmap.generated_at.desc())
        .limit(1)
    )
    roadmap = roadmap_result.scalar_one_or_none()

    # Build milestone info from roadmap
    # milestone_id -> {title, estimated_hours (from daily_tasks)}
    milestone_info: dict[str, dict] = {}
    if roadmap and roadmap.roadmap_json:
        for phase in roadmap.roadmap_json.get("phases", []):
            for ms in phase.get("milestones", []):
                ms_id = ms.get("milestone_id", "")
                # Sum estimated_minutes from all daily_tasks in this milestone
                total_est_minutes = 0
                for task in ms.get("daily_tasks", []):
                    total_est_minutes += task.get("estimated_minutes", 0)
                # Also check milestone-level duration_weeks
                duration_weeks = ms.get("duration_weeks", 0)

                # Priority: daily_tasks sum > duration_weeks * 5h/week > default 30h
                if total_est_minutes > 0:
                    est_hours = total_est_minutes / 60
                elif duration_weeks > 0:
                    est_hours = duration_weeks * 5  # ~5 hours per week
                else:
                    est_hours = DEFAULT_MILESTONE_HOURS

                milestone_info[ms_id] = {
                    "title": ms.get("title", ms_id),
                    "estimated_hours": est_hours,
                }

    # Calculate progress per milestone from linked courses
    milestone_progress: dict[str, dict] = {}

    # Initialize from roadmap milestones (so even 0-progress ones appear)
    for ms_id, info in milestone_info.items():
        milestone_progress[ms_id] = {
            "milestone_id": ms_id,
            "milestone_title": info["title"],
            "total_hours": info["estimated_hours"],
            "completed_hours": 0,
            "course_count": 0,
            "pct": 0,
        }

    # Accumulate from courses
    for c in courses:
        if c.linked_milestone_id:
            if c.linked_milestone_id not in milestone_progress:
                # Course linked to a milestone not in current roadmap
                milestone_progress[c.linked_milestone_id] = {
                    "milestone_id": c.linked_milestone_id,
                    "milestone_title": c.linked_milestone_id,
                    "total_hours": DEFAULT_MILESTONE_HOURS,
                    "completed_hours": 0,
                    "course_count": 0,
                    "pct": 0,
                }
            mp = milestone_progress[c.linked_milestone_id]
            mp["completed_hours"] += c.completed_hours or 0
            mp["course_count"] += 1

    # Calculate percentages
    for mp in milestone_progress.values():
        if mp["total_hours"] > 0:
            mp["pct"] = min(round(mp["completed_hours"] / mp["total_hours"] * 100), 100)

    # Session activity for last 90 days
    cutoff = datetime.utcnow() - timedelta(days=90)
    session_result = await db.execute(
        select(
            func.date(CourseSession.logged_at).label("day"),
            func.sum(CourseSession.duration_minutes).label("minutes"),
        )
        .where(CourseSession.user_id == user.id, CourseSession.logged_at >= cutoff)
        .group_by(func.date(CourseSession.logged_at))
    )
    activity_days = [
        {"date": str(row.day), "minutes": row.minutes}
        for row in session_result.all()
    ]

    return APIResponse(
        data={
            "total_courses": total_courses,
            "platforms": platforms,
            "milestone_progress": list(milestone_progress.values()),
            "activity_days": activity_days,
        }
    )

