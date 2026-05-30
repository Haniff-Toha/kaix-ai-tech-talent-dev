"""
Telegram API — connect, verify, test, disconnect Telegram bot.

POST   /telegram/connect    — Save bot token, validate, start polling
GET    /telegram/status     — Check connection status
DELETE /telegram/disconnect — Remove connection
POST   /telegram/test       — Send a test message
"""

import asyncio
import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.api.deps import CurrentUser, DBSession
from app.db.models import TelegramConnection
from app.schemas import APIResponse
from app.services.telegram_service import (
    format_nudge_telegram,
    poll_for_start,
    send_telegram_message,
    validate_bot_token,
)

logger = logging.getLogger(__name__)
router = APIRouter()


class TelegramConnectRequest(BaseModel):
    bot_token: str = Field(..., min_length=30)


@router.post("/telegram/connect", response_model=APIResponse)
async def connect_telegram(
    request: TelegramConnectRequest,
    user: CurrentUser,
    db: DBSession,
):
    """
    Connect a Telegram bot.
    1. Validate the token with getMe
    2. Save connection
    3. Start background polling for /start
    """
    # Validate token
    bot_info = await validate_bot_token(request.bot_token)
    if not bot_info:
        return APIResponse(
            success=False,
            message="Token tidak valid. Pastikan token dari BotFather benar.",
        )

    bot_username = bot_info.get("username", "")

    # Check existing connection
    result = await db.execute(
        select(TelegramConnection).where(TelegramConnection.user_id == user.id)
    )
    existing = result.scalar_one_or_none()

    if existing:
        existing.bot_token = request.bot_token
        existing.bot_username = bot_username
        existing.chat_id = None
        existing.is_verified = False
        conn = existing
    else:
        conn = TelegramConnection(
            user_id=user.id,
            bot_token=request.bot_token,
            bot_username=bot_username,
        )
        db.add(conn)

    await db.flush()
    await db.refresh(conn)

    # Start background polling to capture /start
    asyncio.create_task(_poll_and_update(str(conn.id), request.bot_token, user.id))

    return APIResponse(
        data={
            "id": str(conn.id),
            "bot_username": bot_username,
            "bot_link": f"https://t.me/{bot_username}",
            "is_verified": False,
            "message": "Bot tervalidasi! Buka link bot di Telegram dan kirim /start",
        },
        message="Bot connected. Kirim /start di Telegram untuk verifikasi.",
    )


async def _poll_and_update(conn_id: str, bot_token: str, user_id):
    """Background task: poll for /start and update chat_id."""
    from app.db.session import async_session as session_factory

    chat_id = await poll_for_start(bot_token, timeout_seconds=120)
    if chat_id:
        async with session_factory() as db:
            result = await db.execute(
                select(TelegramConnection).where(TelegramConnection.id == conn_id)
            )
            conn = result.scalar_one_or_none()
            if conn:
                conn.chat_id = chat_id
                conn.is_verified = True
                await db.commit()

                # Send welcome message
                await send_telegram_message(
                    bot_token,
                    chat_id,
                    "🎉 <b>Koneksi berhasil!</b>\n\n"
                    "Bot ini akan mengirim reminder & notifikasi dari Kaix.\n"
                    "Selamat belajar! 💪",
                )
                logger.info(f"✅ Telegram verified for user {user_id}")


@router.get("/telegram/status", response_model=APIResponse)
async def telegram_status(user: CurrentUser, db: DBSession):
    """Check Telegram connection status."""
    result = await db.execute(
        select(TelegramConnection).where(TelegramConnection.user_id == user.id)
    )
    conn = result.scalar_one_or_none()

    if not conn:
        return APIResponse(data={"connected": False})

    return APIResponse(
        data={
            "connected": True,
            "is_verified": conn.is_verified,
            "bot_username": conn.bot_username,
            "bot_link": f"https://t.me/{conn.bot_username}" if conn.bot_username else None,
            "created_at": conn.created_at.isoformat() if conn.created_at else None,
        }
    )


@router.delete("/telegram/disconnect", response_model=APIResponse)
async def disconnect_telegram(user: CurrentUser, db: DBSession):
    """Remove Telegram connection."""
    result = await db.execute(
        select(TelegramConnection).where(TelegramConnection.user_id == user.id)
    )
    conn = result.scalar_one_or_none()
    if not conn:
        return APIResponse(success=False, message="No Telegram connection found")

    await db.delete(conn)
    await db.flush()
    return APIResponse(message="Telegram disconnected")


@router.post("/telegram/test", response_model=APIResponse)
async def test_telegram(user: CurrentUser, db: DBSession):
    """Send a test message to the user's Telegram bot."""
    result = await db.execute(
        select(TelegramConnection).where(
            TelegramConnection.user_id == user.id,
            TelegramConnection.is_verified == True,  # noqa: E712
        )
    )
    conn = result.scalar_one_or_none()

    if not conn or not conn.chat_id:
        return APIResponse(
            success=False,
            message="Bot belum terverifikasi. Kirim /start di Telegram.",
        )

    test_nudge = {
        "emoji": "🧪",
        "message": "Ini pesan tes dari Kaix! Notifikasi Telegram berhasil.",
    }
    text = format_nudge_telegram(test_nudge, user.name)
    ok = await send_telegram_message(conn.bot_token, conn.chat_id, text)

    if ok:
        return APIResponse(message="Pesan tes terkirim! Cek Telegram-mu.")
    else:
        return APIResponse(success=False, message="Gagal mengirim pesan tes.")
