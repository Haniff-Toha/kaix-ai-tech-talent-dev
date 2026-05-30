"""
Email Service — Brevo SMTP (primary) + Resend (fallback).

Sends notification emails using Brevo SMTP relay.
Falls back to Resend REST API if Brevo fails.
"""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


def _build_html(user_name: str, nudge: dict, context: dict | None = None) -> str:
    """Build a simple, styled email body with rich context."""
    context_section = ""
    if context and (context.get("course_title") or context.get("label")):
        inner_parts = []
        if context.get("label"):
            inner_parts.append(f'<p style="color:#333;font-size:13px;margin:0 0 4px;"><strong>📝 Deskripsi:</strong> {context["label"]}</p>')
        if context.get("course_title"):
            inner_parts.append(f'<p style="color:#4265FF;font-size:13px;margin:0 0 4px;font-weight:600;"><strong>📚 Kursus:</strong> {context["course_title"]}</p>')
        if context.get("course_url"):
            inner_parts.append(f'<p style="margin:4px 0 0;"><a href="{context["course_url"]}" style="color:#4265FF;font-size:12px;">🔗 Buka Kursus</a></p>')
        context_section = f"""
        <div style="background:#EEF2FF;padding:12px 16px;border-radius:8px;margin-bottom:12px;border:1px solid #4265FF;">
            {''.join(inner_parts)}
        </div>
        """

    focus_cta = ""
    if context and context.get("course_title"):
        focus_cta = """
        <p style="color:#333;font-size:14px;text-align:center;margin:0 0 16px;">🎯 Yuk mulai fokus belajar!</p>
        """

    return f"""
    <div style="font-family:'Segoe UI',Arial,sans-serif;max-width:480px;margin:0 auto;padding:24px;background:#FFFDF5;border:2px solid #1A1A2E;border-radius:16px;">
        <div style="text-align:center;margin-bottom:16px;">
            <span style="font-size:48px;">🌿</span>
        </div>
        <h2 style="color:#1A1A2E;font-size:18px;text-align:center;margin:0 0 12px;">
            Kaix Reminder
        </h2>
        {context_section}
        <p style="color:#333;font-size:15px;line-height:1.6;text-align:center;margin:0 0 20px;">
            Hai <strong>{user_name}</strong>,<br/>{nudge.get('message', 'Waktunya belajar!')}
        </p>
        {focus_cta}
        <div style="text-align:center;">
            <a href="http://localhost:5173/focus"
               style="display:inline-block;background:#4265FF;color:#fff;padding:10px 24px;border-radius:8px;text-decoration:none;font-weight:600;border:2px solid #1A1A2E;box-shadow:2px 3px 0 #1A1A2E;">
                Mulai Fokus 🎯
            </a>
        </div>
        <p style="color:#999;font-size:11px;text-align:center;margin:20px 0 0;">
            AI Tech Talent Companion
        </p>
    </div>
    """


def _build_subject(nudge: dict, context: dict | None = None) -> str:
    """Build email subject with context."""
    if context and context.get("course_title"):
        return f"🌿 Reminder: {context['course_title']}"
    if context and context.get("label"):
        return f"🌿 {context['label']}"
    msg = nudge.get('message', 'Kaix Reminder')
    return f"🌿 {msg[:50]}"


async def send_email_brevo(
    to_email: str, user_name: str, nudge: dict, context: dict | None = None
) -> bool:
    """Send email via Brevo SMTP relay."""
    if not settings.brevo_smtp_key:
        logger.warning("Brevo SMTP key not configured, skipping")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = settings.email_from
        msg["To"] = to_email
        msg["Subject"] = _build_subject(nudge, context)

        html = _build_html(user_name, nudge, context)
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(settings.brevo_smtp_host, settings.brevo_smtp_port) as server:
            server.starttls()
            server.login(settings.brevo_smtp_login, settings.brevo_smtp_key)
            server.send_message(msg)

        logger.info(f"✉️ Email sent via Brevo to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Brevo SMTP failed: {e}")
        return False


async def send_email_resend(
    to_email: str, user_name: str, nudge: dict, context: dict | None = None
) -> bool:
    """Fallback: Send email via Resend REST API."""
    if not settings.resend_api_key:
        logger.warning("Resend API key not configured, skipping")
        return False

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {settings.resend_api_key}"},
                json={
                    "from": "Kaix <onboarding@resend.dev>",
                    "to": [to_email],
                    "subject": _build_subject(nudge, context),
                    "html": _build_html(user_name, nudge, context),
                },
            )
            if resp.status_code in (200, 201):
                logger.info(f"✉️ Email sent via Resend to {to_email}")
                return True
            else:
                logger.error(f"Resend failed: {resp.status_code} {resp.text}")
                return False
    except Exception as e:
        logger.error(f"Resend failed: {e}")
        return False


async def send_email(
    to_email: str, user_name: str, nudge: dict, context: dict | None = None
) -> bool:
    """Send email — try Brevo first, fall back to Resend."""
    ok = await send_email_brevo(to_email, user_name, nudge, context)
    if not ok:
        logger.info("Falling back to Resend...")
        ok = await send_email_resend(to_email, user_name, nudge, context)
    return ok
