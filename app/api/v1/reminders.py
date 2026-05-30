"""
Reminders CRUD + Nudge preview.

POST   /reminders                  — Create a reminder
GET    /reminders                  — List user's reminders
PATCH  /reminders/{id}             — Update reminder
DELETE /reminders/{id}             — Delete reminder
POST   /reminders/{id}/preview     — Preview nudge message
"""

import logging
import uuid
from datetime import time

from fastapi import APIRouter

from app.agents.nudge_agent import generate_nudge
from app.api.deps import CurrentUser, DBSession
from app.db.models import Reminder
from app.schemas import (
    APIResponse,
    ReminderRequest,
    ReminderResponse,
    ReminderUpdateRequest,
)
from sqlalchemy import select

logger = logging.getLogger(__name__)
router = APIRouter()


def _serialize_reminder(reminder: Reminder) -> dict:
    """Serialize reminder with time as HH:MM string."""
    data = {
        "id": str(reminder.id),
        "user_id": str(reminder.user_id),
        "type": reminder.type,
        "channel": reminder.channel,
        "scheduled_time": reminder.scheduled_time.strftime("%H:%M")
        if reminder.scheduled_time
        else None,
        "days": reminder.days,
        "timezone": reminder.timezone,
        "is_active": reminder.is_active,
        "label": reminder.label,
        "linked_course_id": str(reminder.linked_course_id) if reminder.linked_course_id else None,
        "last_sent_at": reminder.last_sent_at.isoformat() if reminder.last_sent_at else None,
        "created_at": reminder.created_at.isoformat() if reminder.created_at else None,
    }
    return data


@router.post("/reminders", response_model=APIResponse)
async def create_reminder(
    request: ReminderRequest,
    user: CurrentUser,
    db: DBSession,
):
    """Create a reminder."""
    # Parse time string "HH:MM" to time object
    hour, minute = map(int, request.scheduled_time.split(":"))
    scheduled = time(hour=hour, minute=minute)

    reminder = Reminder(
        user_id=user.id,
        type=request.type,
        channel=request.channel,
        scheduled_time=scheduled,
        days=request.days,
        timezone=request.timezone,
        label=request.label,
        linked_course_id=request.linked_course_id,
    )
    db.add(reminder)
    await db.flush()

    return APIResponse(
        data=_serialize_reminder(reminder),
        message="Pengingat dibuat! / Reminder created!",
    )


@router.get("/reminders", response_model=APIResponse)
async def list_reminders(user: CurrentUser, db: DBSession):
    """Get all user reminders."""
    result = await db.execute(
        select(Reminder)
        .where(Reminder.user_id == user.id)
        .order_by(Reminder.created_at.desc())
    )
    reminders = result.scalars().all()

    return APIResponse(
        data=[_serialize_reminder(r) for r in reminders]
    )


@router.patch("/reminders/{reminder_id}", response_model=APIResponse)
async def update_reminder(
    reminder_id: uuid.UUID,
    request: ReminderUpdateRequest,
    user: CurrentUser,
    db: DBSession,
):
    """Update reminder settings."""
    reminder = await db.get(Reminder, reminder_id)
    if not reminder or reminder.user_id != user.id:
        return APIResponse(
            success=False,
            message="Pengingat tidak ditemukan / Reminder not found",
        )

    update_data = request.model_dump(exclude_unset=True)

    # Handle time string conversion
    if "scheduled_time" in update_data and update_data["scheduled_time"]:
        hour, minute = map(int, update_data["scheduled_time"].split(":"))
        update_data["scheduled_time"] = time(hour=hour, minute=minute)

    for field, value in update_data.items():
        setattr(reminder, field, value)

    await db.flush()

    return APIResponse(
        data=_serialize_reminder(reminder),
        message="Pengingat diperbarui / Reminder updated",
    )


@router.delete("/reminders/{reminder_id}", response_model=APIResponse)
async def delete_reminder(
    reminder_id: uuid.UUID,
    user: CurrentUser,
    db: DBSession,
):
    """Delete a reminder."""
    reminder = await db.get(Reminder, reminder_id)
    if not reminder or reminder.user_id != user.id:
        return APIResponse(
            success=False,
            message="Pengingat tidak ditemukan / Reminder not found",
        )

    await db.delete(reminder)
    await db.flush()
    return APIResponse(message="Pengingat dihapus / Reminder deleted")


@router.post("/reminders/{reminder_id}/preview", response_model=APIResponse)
async def preview_nudge(
    reminder_id: uuid.UUID,
    user: CurrentUser,
    db: DBSession,
):
    """
    Preview what the nudge message will say.

    Generates an AI message using the reminder type and user context
    without actually sending it.
    """
    reminder = await db.get(Reminder, reminder_id)
    if not reminder or reminder.user_id != user.id:
        return APIResponse(
            success=False,
            message="Pengingat tidak ditemukan / Reminder not found",
        )

    nudge = await generate_nudge(
        db=db,
        user=user,
        nudge_type=reminder.type,
    )

    return APIResponse(
        data={
            "reminder": _serialize_reminder(reminder),
            "preview": nudge,
        },
        message="Preview nudge berhasil / Nudge preview generated",
    )
