"""
Overview / Dashboard endpoints.

GET    /overview       — Aggregated dashboard (streak, tasks, progress, logs, quote)
POST   /overview/notes — Save a quick note
GET    /overview/notes — Get user's notes
DELETE /overview/notes/{id} — Delete a note
"""

import logging
import uuid
from datetime import date

from fastapi import APIRouter

from app.api.deps import CurrentUser, DBSession
from app.db.models import ActivityLog, Note, Roadmap, Streak
from app.schemas import (
    APIResponse,
    ActivityLogResponse,
    NoteRequest,
    NoteResponse,
    OverviewResponse,
    StreakResponse,
)
from sqlalchemy import select

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/overview", response_model=APIResponse)
async def get_overview(user: CurrentUser, db: DBSession):
    """
    Aggregated dashboard data.

    Returns: streak, today's tasks, milestone progress, recent logs, daily quote.
    """
    # Streak
    streak = await db.get(Streak, user.id)
    streak_data = (
        StreakResponse.model_validate(streak).model_dump()
        if streak
        else {"current_streak": 0, "longest_streak": 0, "last_activity_date": None}
    )

    # Active roadmap
    result = await db.execute(
        select(Roadmap)
        .where(Roadmap.user_id == user.id, Roadmap.is_active == True)  # noqa: E712
        .order_by(Roadmap.generated_at.desc())
        .limit(1)
    )
    roadmap = result.scalar_one_or_none()

    today_tasks = []
    milestone_progress = []
    daily_quote = None
    active_phase = None

    if roadmap and roadmap.roadmap_json:
        roadmap_data = roadmap.roadmap_json
        daily_quote = roadmap_data.get("daily_quote")

        # Extract today's tasks and milestone progress from roadmap JSON
        for phase in roadmap_data.get("phases", []):
            for ms in phase.get("milestones", []):
                milestone_progress.append({
                    "milestone_id": ms.get("milestone_id"),
                    "title": ms.get("title"),
                    "phase_number": phase.get("phase_number"),
                    "progress_pct": 0,  # Will be calculated from activity logs
                })

                # Grab first few tasks as today's tasks
                for task in ms.get("daily_tasks", [])[:2]:
                    if len(today_tasks) < 5:
                        today_tasks.append(task)

        # Get first active phase
        phases = roadmap_data.get("phases", [])
        if phases:
            active_phase = {
                "phase_number": phases[0].get("phase_number"),
                "title": phases[0].get("phase_title"),
                "progress_pct": 0,
            }

    # Calculate milestone progress from activity logs
    if milestone_progress:
        for mp in milestone_progress:
            result = await db.execute(
                select(ActivityLog)
                .where(
                    ActivityLog.user_id == user.id,
                    ActivityLog.mapped_milestone_id == mp["milestone_id"],
                    ActivityLog.confirmed == True,  # noqa: E712
                )
            )
            logs = result.scalars().all()
            total_delta = sum(log.milestone_progress_delta for log in logs)
            mp["progress_pct"] = min(round(total_delta * 100, 1), 100)

    # Recent activity logs (last 10)
    result = await db.execute(
        select(ActivityLog)
        .where(ActivityLog.user_id == user.id)
        .order_by(ActivityLog.logged_at.desc())
        .limit(10)
    )
    recent_logs_raw = result.scalars().all()
    recent_logs = [
        ActivityLogResponse.model_validate(log).model_dump(mode="json")
        for log in recent_logs_raw
    ]

    return APIResponse(
        data=OverviewResponse(
            streak=streak_data,
            today_tasks=today_tasks,
            milestone_progress=milestone_progress,
            recent_logs=recent_logs,
            daily_quote=daily_quote,
            active_phase=active_phase,
        ).model_dump(mode="json")
    )


# ─── Notes ───

@router.post("/overview/notes", response_model=APIResponse)
async def create_note(
    request: NoteRequest,
    user: CurrentUser,
    db: DBSession,
):
    """Save a quick note."""
    note = Note(user_id=user.id, content=request.content)
    db.add(note)
    await db.flush()
    return APIResponse(
        data=NoteResponse.model_validate(note).model_dump(mode="json"),
        message="Catatan disimpan / Note saved",
    )


@router.get("/overview/notes", response_model=APIResponse)
async def get_notes(user: CurrentUser, db: DBSession):
    """Get all user notes."""
    result = await db.execute(
        select(Note)
        .where(Note.user_id == user.id)
        .order_by(Note.created_at.desc())
    )
    notes = result.scalars().all()
    return APIResponse(
        data=[
            NoteResponse.model_validate(n).model_dump(mode="json")
            for n in notes
        ]
    )


@router.delete("/overview/notes/{note_id}", response_model=APIResponse)
async def delete_note(
    note_id: uuid.UUID,
    user: CurrentUser,
    db: DBSession,
):
    """Delete a note."""
    note = await db.get(Note, note_id)
    if not note or note.user_id != user.id:
        return APIResponse(
            success=False,
            message="Catatan tidak ditemukan / Note not found",
        )

    await db.delete(note)
    await db.flush()
    return APIResponse(message="Catatan dihapus / Note deleted")
