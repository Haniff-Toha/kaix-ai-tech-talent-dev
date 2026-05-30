"""
Notifications API — in-app notification feed.

GET    /notifications           — List user notifications (paginated)
PATCH  /notifications/{id}/read — Mark one as read
POST   /notifications/read-all  — Mark all as read
GET    /notifications/unread-count — Badge count
"""

import logging
import uuid

from fastapi import APIRouter, Query
from sqlalchemy import func, select, update

from app.api.deps import CurrentUser, DBSession
from app.db.models import Notification
from app.schemas import APIResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/notifications", response_model=APIResponse)
async def list_notifications(
    user: CurrentUser,
    db: DBSession,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=50),
):
    """List user's in-app notifications, newest first."""
    offset = (page - 1) * per_page

    total = (
        await db.execute(
            select(func.count(Notification.id)).where(Notification.user_id == user.id)
        )
    ).scalar()

    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == user.id)
        .order_by(Notification.created_at.desc())
        .offset(offset)
        .limit(per_page)
    )
    notifications = result.scalars().all()

    return APIResponse(
        data={
            "items": [
                {
                    "id": str(n.id),
                    "title": n.title,
                    "body": n.body,
                    "channel": n.channel,
                    "is_read": n.is_read,
                    "created_at": n.created_at.isoformat() if n.created_at else None,
                }
                for n in notifications
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
        }
    )


@router.patch("/notifications/{notification_id}/read", response_model=APIResponse)
async def mark_notification_read(
    notification_id: uuid.UUID,
    user: CurrentUser,
    db: DBSession,
):
    """Mark a single notification as read."""
    notification = await db.get(Notification, notification_id)
    if not notification or notification.user_id != user.id:
        return APIResponse(success=False, message="Notification not found")

    notification.is_read = True
    await db.flush()
    return APIResponse(message="Marked as read")


@router.post("/notifications/read-all", response_model=APIResponse)
async def mark_all_read(user: CurrentUser, db: DBSession):
    """Mark all user notifications as read."""
    await db.execute(
        update(Notification)
        .where(Notification.user_id == user.id, Notification.is_read == False)  # noqa: E712
        .values(is_read=True)
    )
    await db.flush()
    return APIResponse(message="All notifications marked as read")


@router.get("/notifications/unread-count", response_model=APIResponse)
async def unread_count(user: CurrentUser, db: DBSession):
    """Get unread notification count for badge."""
    count = (
        await db.execute(
            select(func.count(Notification.id)).where(
                Notification.user_id == user.id,
                Notification.is_read == False,  # noqa: E712
            )
        )
    ).scalar()

    return APIResponse(data={"count": count or 0})
