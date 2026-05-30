"""
Nudge Agent — generates personalized reminder messages.

Responsibilities:
    - Generate motivational nudge messages per user context
    - Vary message style daily (never repeat same opening)
    - Support multiple nudge types: daily_task, streak_at_risk,
      procrastination, weekly_recap, encouragement

Model: Fast LLM (gemma-3-27b-it via Groq)
"""

import logging

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.llm import fast_llm
from app.db.models import Profile, Roadmap, Streak, User
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

llm = LLMService(primary=fast_llm, name="nudge_agent")


# ──────────────────────────────────────────────
# Structured output schema
# ──────────────────────────────────────────────
class NudgeMessage(BaseModel):
    """Generated nudge/reminder message."""
    message: str = Field(description="The nudge message, max 120 characters, personal and motivating")
    emoji: str = Field(description="A single relevant emoji for the message")
    tone: str = Field(description="The tone used: encouraging, urgent, celebratory, casual")


# ──────────────────────────────────────────────
# System prompts
# ──────────────────────────────────────────────
SYSTEM_PROMPT_ID = """Kamu adalah Nudge Agent untuk Kaix, aplikasi pengembangan karir.

Tugasmu membuat pesan pengingat pendek yang personal dan memotivasi.

Aturan:
1. Pesan MAKSIMAL 120 karakter
2. Gunakan nama pengguna jika ada
3. Referensikan progress, streak, atau task terbaru mereka
4. JANGAN pernah pakai pembuka yang sama berturut-turut
5. Variasikan gaya: kadang santai, kadang serius, kadang lucu
6. Selalu dalam Bahasa Indonesia
7. Gunakan emoji yang mindful & learning: 🌿 📚 🌟 🌾 🎯 🌱 🌻 ✨ 📖
8. JANGAN gunakan emoji otot (💪), api (🔥), atau emoji yang agresif

Tipe nudge:
- daily_task: Ingatkan task hari ini
- streak_at_risk: Streak hampir putus, motivasi untuk belajar
- procrastination: Gentle push untuk yang belum mulai hari ini
- weekly_recap: Rangkuman minggu ini
- encouragement: Pujian untuk progress yang bagus"""

SYSTEM_PROMPT_EN = """You are the Nudge Agent for Kaix, a career development app.

Your job is to create short, personal, motivating reminder messages.

Rules:
1. Message MUST be 120 characters or fewer
2. Use the user's name if available
3. Reference their progress, streak, or current task
4. NEVER use the same opening pattern on consecutive messages
5. Vary style: sometimes casual, sometimes serious, sometimes humorous
6. Always in English

Nudge types:
- daily_task: Remind about today's task
- streak_at_risk: Streak about to break, motivate to study
- procrastination: Gentle push for those who haven't started today
- weekly_recap: This week's summary
- encouragement: Praise for good progress"""


async def generate_nudge(
    db: AsyncSession,
    user: User,
    nudge_type: str = "daily_task",
) -> dict:
    """
    Generate a personalized nudge message.

    Args:
        db: Database session
        user: The user to nudge
        nudge_type: Type of nudge (daily_task, streak_at_risk, etc.)

    Returns:
        dict with message, emoji, and tone
    """
    locale = user.locale or "id"
    system_prompt = SYSTEM_PROMPT_ID if locale == "id" else SYSTEM_PROMPT_EN

    # Gather context
    profile = await db.get(Profile, user.id)
    streak = await db.get(Streak, user.id)

    # Get active roadmap for today's task
    result = await db.execute(
        select(Roadmap)
        .where(Roadmap.user_id == user.id, Roadmap.is_active == True)  # noqa: E712
        .order_by(Roadmap.generated_at.desc())
        .limit(1)
    )
    roadmap = result.scalar_one_or_none()

    # Extract today's task from roadmap
    today_task = None
    if roadmap and roadmap.roadmap_json:
        for phase in roadmap.roadmap_json.get("phases", []):
            for ms in phase.get("milestones", []):
                tasks = ms.get("daily_tasks", [])
                if tasks:
                    today_task = tasks[0].get("title", "")
                    break
            if today_task:
                break

    context = f"""
User: {user.name}
Nudge type: {nudge_type}
Current streak: {streak.current_streak if streak else 0} days
Longest streak: {streak.longest_streak if streak else 0} days
Target role: {profile.target_role if profile else 'Unknown'}
Today's task: {today_task or 'No specific task'}
Experience level: {profile.experience_level if profile else 'beginner'}
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Generate a {nudge_type} nudge for this user:\n{context}"),
    ]

    try:
        result = await llm.ainvoke_with_structured_output(messages, schema=NudgeMessage)
        return {
            "message": result.message[:120],  # enforce limit
            "emoji": result.emoji,
            "tone": result.tone,
            "nudge_type": nudge_type,
        }
    except Exception as e:
        logger.error(f"Nudge generation failed: {e}")
        # Fallback static messages
        fallbacks = {
            "daily_task": f"Hey {user.name}, waktunya belajar hari ini! 💪",
            "streak_at_risk": f"{user.name}, streak-mu hampir putus! Yuk luangkan 15 menit 🔥",
            "procrastination": f"Belum mulai hari ini, {user.name}? 15 menit aja dulu! 🚀",
            "encouragement": f"Great progress, {user.name}! Terus semangat! ⭐",
            "weekly_recap": f"Minggu yang produktif, {user.name}! 📊",
        }
        return {
            "message": fallbacks.get(nudge_type, f"Yuk belajar, {user.name}! 💪"),
            "emoji": "💪",
            "tone": "encouraging",
            "nudge_type": nudge_type,
        }
