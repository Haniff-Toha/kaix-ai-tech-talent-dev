"""
Notification Service — unified dispatcher for all channels.

Routes nudge messages to in_app, email, or telegram based on reminder.channel.
Enriches notification content with explicit Course/Description labels.
"""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Notification, TelegramConnection, User
from app.services.email_service import send_email
from app.services.telegram_service import format_nudge_telegram, send_telegram_message
from sqlalchemy import select

logger = logging.getLogger(__name__)

# Mindful learning emojis (no muscle emojis)
EMOJI_MAP = {
    "daily_task": "🌿",
    "course": "📚",
    "streak_at_risk": "🔥",
    "weekly_recap": "📊",
    "encouragement": "🌟",
    "procrastination": "🍃",
}


def _pick_emoji(context: dict | None) -> str:
    """Pick an appropriate emoji based on context type."""
    if context and context.get("type"):
        return EMOJI_MAP.get(context["type"], "🌿")
    return "🌿"


def _build_title(nudge: dict, context: dict | None) -> str:
    """Build a rich notification title from context."""
    emoji = _pick_emoji(context)

    if context:
        if context.get("course_title"):
            return f"{emoji} Reminder: {context['course_title']}"
        if context.get("label"):
            return f"{emoji} {context['label']}"

    return f"{emoji} Kaix Reminder"


def _build_body(nudge: dict, context: dict | None) -> str:
    """Build a rich notification body with explicit labeled sections."""
    message = nudge.get("message", "Waktunya belajar!")
    lines = []

    if context:
        # Explicit description label
        if context.get("label"):
            lines.append(f"📝 Deskripsi: {context['label']}")

        # Explicit course label
        if context.get("course_title"):
            lines.append(f"📚 Kursus: {context['course_title']}")

        # Course URL
        if context.get("course_url"):
            lines.append(f"🔗 Link: {context['course_url']}")

        # CTA for course-related
        if context.get("course_title"):
            lines.append("🎯 Yuk mulai fokus belajar!")

        if lines:
            lines.append("---")

    lines.append(message)

    return "\n".join(lines)


async def send_in_app(
    db: AsyncSession, user: User, nudge: dict, reminder_id=None, context: dict | None = None
) -> bool:
    """Store notification in the database for in-app feed."""
    try:
        notification = Notification(
            user_id=user.id,
            reminder_id=reminder_id,
            title=_build_title(nudge, context),
            body=_build_body(nudge, context),
            channel="in_app",
        )
        db.add(notification)
        await db.flush()
        logger.info(f"🔔 In-app notification stored for {user.name}")
        return True
    except Exception as e:
        logger.error(f"In-app notification failed: {e}")
        return False


async def send_via_email(user: User, nudge: dict, context: dict | None = None) -> bool:
    """Send notification via email."""
    return await send_email(user.email, user.name, nudge, context)


async def send_via_telegram(
    db: AsyncSession, user: User, nudge: dict, context: dict | None = None
) -> bool:
    """Send notification via Telegram bot."""
    result = await db.execute(
        select(TelegramConnection).where(
            TelegramConnection.user_id == user.id,
            TelegramConnection.is_verified == True,  # noqa: E712
        )
    )
    conn = result.scalar_one_or_none()
    if not conn or not conn.chat_id:
        logger.warning(f"No verified Telegram connection for {user.name}")
        return False

    text = format_nudge_telegram(nudge, user.name, context)
    return await send_telegram_message(conn.bot_token, conn.chat_id, text)


async def dispatch_notification(
    db: AsyncSession, user: User, channel: str, nudge: dict,
    reminder_id=None, context: dict | None = None
) -> bool:
    """
    Dispatch a notification to the appropriate channel.

    Args:
        db: Database session
        user: Target user
        channel: One of 'in_app', 'email', 'telegram'
        nudge: Dict with message, emoji, tone
        reminder_id: Optional reminder FK
        context: Optional dict with label, course_title, course_url, type
    """
    # Always create in-app record
    await send_in_app(db, user, nudge, reminder_id, context)

    if channel == "email":
        return await send_via_email(user, nudge, context)
    elif channel == "telegram":
        return await send_via_telegram(db, user, nudge, context)
    else:
        # in_app is already handled above
        return True
