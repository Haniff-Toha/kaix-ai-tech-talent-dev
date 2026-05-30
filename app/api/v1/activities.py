"""
Activity logging endpoints.

POST  /activities              — Log an activity (→ Logging Classifier)
GET   /activities              — List activity history
PATCH /activities/{id}/confirm — Confirm a low-confidence classification
"""

import logging
import uuid

from fastapi import APIRouter, Query

from app.agents.logging_classifier import run_logging_classifier
from app.api.deps import CurrentUser, DBSession
from app.db.models import ActivityLog
from app.schemas import (
    APIResponse,
    ActivityConfirmRequest,
    ActivityLogRequest,
    ActivityLogResponse,
)
from sqlalchemy import select, func

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/activities", response_model=APIResponse)
async def log_activity(
    request: ActivityLogRequest,
    user: CurrentUser,
    db: DBSession,
):
    """
    Log a learning activity.

    The Logging Classifier will:
    - Parse the free-text description
    - Map it to the most relevant milestone
    - Calculate progress delta
    - Update streak
    """
    result = await run_logging_classifier(
        db=db,
        user=user,
        raw_text=request.raw_text,
        duration_minutes=request.duration_minutes,
    )

    return APIResponse(data=result)


@router.get("/activities", response_model=APIResponse)
async def list_activities(
    user: CurrentUser,
    db: DBSession,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=50),
):
    """Get paginated activity history for the current user."""
    offset = (page - 1) * per_page

    # Get total count
    count_result = await db.execute(
        select(func.count(ActivityLog.id)).where(ActivityLog.user_id == user.id)
    )
    total = count_result.scalar()

    # Get logs
    result = await db.execute(
        select(ActivityLog)
        .where(ActivityLog.user_id == user.id)
        .order_by(ActivityLog.logged_at.desc())
        .offset(offset)
        .limit(per_page)
    )
    logs = result.scalars().all()

    return APIResponse(
        data={
            "items": [
                ActivityLogResponse.model_validate(log).model_dump(mode="json")
                for log in logs
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
        }
    )


@router.patch("/activities/{activity_id}/confirm", response_model=APIResponse)
async def confirm_activity(
    activity_id: uuid.UUID,
    request: ActivityConfirmRequest,
    user: CurrentUser,
    db: DBSession,
):
    """
    Confirm a low-confidence activity classification.

    When the Logging Classifier has confidence < 0.6, the user picks the correct milestone.
    """
    log = await db.get(ActivityLog, activity_id)
    if not log or log.user_id != user.id:
        return APIResponse(
            success=False,
            message="Aktivitas tidak ditemukan / Activity not found",
        )

    log.mapped_milestone_id = request.milestone_id
    log.confirmed = True
    log.needs_confirmation = False
    await db.flush()

    return APIResponse(
        data=ActivityLogResponse.model_validate(log).model_dump(mode="json"),
        message="Klasifikasi dikonfirmasi / Classification confirmed",
    )
