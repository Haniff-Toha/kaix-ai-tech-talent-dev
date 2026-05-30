"""
Telegram Service — send messages via Telegram Bot API.

Handles bot validation, chat_id resolution (polling), and message sending.
"""

import asyncio
import logging

import httpx

logger = logging.getLogger(__name__)

TG_API = "https://api.telegram.org"


async def validate_bot_token(bot_token: str) -> dict | None:
    """Validate a bot token by calling getMe. Returns bot info or None."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{TG_API}/bot{bot_token}/getMe")
            data = resp.json()
            if data.get("ok"):
                return data["result"]
    except Exception as e:
        logger.error(f"Telegram getMe failed: {e}")
    return None


async def poll_for_start(bot_token: str, timeout_seconds: int = 60) -> str | None:
    """
    Poll getUpdates for up to timeout_seconds to capture a /start message.
    Returns the chat_id if found, None otherwise.
    """
    logger.info(f"Polling Telegram for /start (timeout={timeout_seconds}s)")
    offset = 0
    deadline = asyncio.get_event_loop().time() + timeout_seconds

    async with httpx.AsyncClient(timeout=15) as client:
        while asyncio.get_event_loop().time() < deadline:
            try:
                resp = await client.get(
                    f"{TG_API}/bot{bot_token}/getUpdates",
                    params={"offset": offset, "timeout": 5, "allowed_updates": '["message"]'},
                )
                data = resp.json()
                if data.get("ok"):
                    for update in data.get("result", []):
                        offset = update["update_id"] + 1
                        msg = update.get("message", {})
                        text = msg.get("text", "")
                        if text.strip() == "/start":
                            chat_id = str(msg["chat"]["id"])
                            logger.info(f"✅ Captured Telegram chat_id: {chat_id}")
                            return chat_id
            except Exception as e:
                logger.warning(f"Telegram poll error: {e}")
            await asyncio.sleep(2)

    logger.warning("Telegram polling timed out — no /start received")
    return None


async def send_telegram_message(
    bot_token: str, chat_id: str, text: str, parse_mode: str = "HTML"
) -> bool:
    """Send a message via Telegram Bot API."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{TG_API}/bot{bot_token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": parse_mode,
                },
            )
            data = resp.json()
            if data.get("ok"):
                logger.info(f"📨 Telegram message sent to chat {chat_id}")
                return True
            else:
                logger.error(f"Telegram sendMessage failed: {data}")
                return False
    except Exception as e:
        logger.error(f"Telegram send failed: {e}")
        return False


def format_nudge_telegram(nudge: dict, user_name: str, context: dict | None = None) -> str:
    """Format a nudge message for Telegram with explicit labeled sections."""
    message = nudge.get("message", "Waktunya belajar!")

    lines = ["🌿 <b>Kaix Reminder</b>", ""]

    if context:
        # Explicit description label
        if context.get("label"):
            lines.append(f"📝 <b>Deskripsi:</b> {context['label']}")

        # Explicit course label
        if context.get("course_title"):
            lines.append(f"📚 <b>Kursus:</b> {context['course_title']}")

        # Course URL
        if context.get("course_url"):
            lines.append(f"🔗 <a href=\"{context['course_url']}\">Buka Kursus</a>")

        # CTA
        if context.get("course_title"):
            lines.append("")
            lines.append("🎯 Yuk mulai fokus belajar!")

        lines.append("")

    lines.append(f"Hai {user_name},")
    lines.append(message)
    lines.append("")
    lines.append("<i>🌿 AI Tech Talent Companion</i>")

    return "\n".join(lines)
