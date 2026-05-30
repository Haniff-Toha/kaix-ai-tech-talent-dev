"""
Stats endpoints — aggregated learning statistics.

GET /stats/streak   — Current and longest streak
GET /stats/progress — Milestone completion % across all phases
GET /stats/time     — Total study hours (daily, weekly, monthly)
"""

import logging
from datetime import date, timedelta

from fastapi import APIRouter

from app.api.deps import CurrentUser, DBSession
from app.db.models import ActivityLog, CourseSession, Roadmap, Streak
from app.schemas import APIResponse
from sqlalchemy import func, select

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/stats/streak", response_model=APIResponse)
async def get_streak_stats(user: CurrentUser, db: DBSession):
    """Get current and longest streak, plus total study minutes and milestones completed."""
    streak = await db.get(Streak, user.id)

    # Total study minutes from activity logs + course sessions
    result_al = await db.execute(
        select(func.coalesce(func.sum(ActivityLog.duration_minutes), 0))
        .where(ActivityLog.user_id == user.id)
    )
    result_cs = await db.execute(
        select(func.coalesce(func.sum(CourseSession.duration_minutes), 0))
        .where(CourseSession.user_id == user.id)
    )
    total_study_minutes = (result_al.scalar() or 0) + (result_cs.scalar() or 0)

    # Milestones completed (progress >= 1.0 means 100%)
    milestones_completed = 0
    result_rm = await db.execute(
        select(Roadmap)
        .where(Roadmap.user_id == user.id, Roadmap.is_active == True)  # noqa: E712
        .order_by(Roadmap.generated_at.desc())
        .limit(1)
    )
    roadmap = result_rm.scalar_one_or_none()
    if roadmap and roadmap.roadmap_json:
        for phase in roadmap.roadmap_json.get("phases", []):
            for ms in phase.get("milestones", []):
                ms_id = ms.get("milestone_id")
                result_delta = await db.execute(
                    select(func.coalesce(func.sum(ActivityLog.milestone_progress_delta), 0))
                    .where(
                        ActivityLog.user_id == user.id,
                        ActivityLog.mapped_milestone_id == ms_id,
                        ActivityLog.confirmed == True,  # noqa: E712
                    )
                )
                if (result_delta.scalar() or 0) >= 1.0:
                    milestones_completed += 1

    return APIResponse(
        data={
            "current_streak": streak.current_streak if streak else 0,
            "longest_streak": streak.longest_streak if streak else 0,
            "last_activity_date": (
                streak.last_activity_date.isoformat() if streak and streak.last_activity_date else None
            ),
            "total_study_minutes": total_study_minutes,
            "milestones_completed": milestones_completed,
        }
    )


@router.get("/stats/progress", response_model=APIResponse)
async def get_progress_stats(user: CurrentUser, db: DBSession):
    """
    Get milestone completion percentages across all phases.

    Computes progress from confirmed activity log deltas.
    """
    # Get active roadmap
    result = await db.execute(
        select(Roadmap)
        .where(Roadmap.user_id == user.id, Roadmap.is_active == True)  # noqa: E712
        .order_by(Roadmap.generated_at.desc())
        .limit(1)
    )
    roadmap = result.scalar_one_or_none()

    if not roadmap or not roadmap.roadmap_json:
        return APIResponse(
            data={"phases": [], "overall_progress_pct": 0},
            message="Belum ada roadmap / No roadmap yet",
        )

    phases_data = []
    total_milestones = 0
    total_progress = 0.0

    for phase in roadmap.roadmap_json.get("phases", []):
        milestones_data = []
        for ms in phase.get("milestones", []):
            ms_id = ms.get("milestone_id")

            # Sum confirmed deltas for this milestone
            result = await db.execute(
                select(func.coalesce(func.sum(ActivityLog.milestone_progress_delta), 0))
                .where(
                    ActivityLog.user_id == user.id,
                    ActivityLog.mapped_milestone_id == ms_id,
                    ActivityLog.confirmed == True,  # noqa: E712
                )
            )
            raw_progress = result.scalar()
            progress_pct = min(round(raw_progress * 100, 1), 100)

            milestones_data.append({
                "milestone_id": ms_id,
                "title": ms.get("title"),
                "progress_pct": progress_pct,
                "skills": ms.get("skills", []),
            })
            total_milestones += 1
            total_progress += progress_pct

        phases_data.append({
            "phase_number": phase.get("phase_number"),
            "phase_title": phase.get("phase_title"),
            "milestones": milestones_data,
            "phase_progress_pct": round(
                sum(m["progress_pct"] for m in milestones_data) / max(len(milestones_data), 1),
                1,
            ),
        })

    overall = round(total_progress / max(total_milestones, 1), 1)

    return APIResponse(
        data={
            "phases": phases_data,
            "overall_progress_pct": overall,
            "total_milestones": total_milestones,
        }
    )


@router.get("/stats/time", response_model=APIResponse)
async def get_time_stats(user: CurrentUser, db: DBSession):
    """
    Get total study hours logged — daily (last 7 days), weekly (last 4), and all-time.

    Combines ActivityLog duration_minutes + CourseSession duration_minutes.
    """
    today = date.today()

    # ── Daily breakdown (last 7 days) ──
    daily = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)

        # Activity logs
        result_al = await db.execute(
            select(func.coalesce(func.sum(ActivityLog.duration_minutes), 0))
            .where(
                ActivityLog.user_id == user.id,
                func.date(ActivityLog.logged_at) == day,
            )
        )
        al_minutes = result_al.scalar()

        # Course sessions
        result_cs = await db.execute(
            select(func.coalesce(func.sum(CourseSession.duration_minutes), 0))
            .where(
                CourseSession.user_id == user.id,
                func.date(CourseSession.logged_at) == day,
            )
        )
        cs_minutes = result_cs.scalar()

        total_minutes = (al_minutes or 0) + (cs_minutes or 0)
        daily.append({
            "date": day.isoformat(),
            "minutes": total_minutes,
            "hours": round(total_minutes / 60, 1),
        })

    # ── Weekly totals (last 4 weeks) ──
    weekly = []
    for w in range(3, -1, -1):
        week_start = today - timedelta(days=today.weekday() + 7 * w)
        week_end = week_start + timedelta(days=6)

        result_al = await db.execute(
            select(func.coalesce(func.sum(ActivityLog.duration_minutes), 0))
            .where(
                ActivityLog.user_id == user.id,
                func.date(ActivityLog.logged_at) >= week_start,
                func.date(ActivityLog.logged_at) <= week_end,
            )
        )
        al_min = result_al.scalar()

        result_cs = await db.execute(
            select(func.coalesce(func.sum(CourseSession.duration_minutes), 0))
            .where(
                CourseSession.user_id == user.id,
                func.date(CourseSession.logged_at) >= week_start,
                func.date(CourseSession.logged_at) <= week_end,
            )
        )
        cs_min = result_cs.scalar()

        total = (al_min or 0) + (cs_min or 0)
        weekly.append({
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "minutes": total,
            "hours": round(total / 60, 1),
        })

    # ── All-time total ──
    result_al_total = await db.execute(
        select(func.coalesce(func.sum(ActivityLog.duration_minutes), 0))
        .where(ActivityLog.user_id == user.id)
    )
    result_cs_total = await db.execute(
        select(func.coalesce(func.sum(CourseSession.duration_minutes), 0))
        .where(CourseSession.user_id == user.id)
    )
    total_all_time = (result_al_total.scalar() or 0) + (result_cs_total.scalar() or 0)

    # ── Activity count ──
    result_count = await db.execute(
        select(func.count(ActivityLog.id)).where(ActivityLog.user_id == user.id)
    )
    total_activities = result_count.scalar()

    return APIResponse(
        data={
            "daily": daily,
            "weekly": weekly,
            "all_time": {
                "minutes": total_all_time,
                "hours": round(total_all_time / 60, 1),
            },
            "total_activities": total_activities,
        }
    )
