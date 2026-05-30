"""
Profile Agent — processes onboarding data into structured profile.

Responsibilities:
    - Parse raw onboarding form into normalized profile JSON
    - Compute gap_score between current skills and target role
    - Store profile in DB
    - Embed profile into User RAG for future context

Model: Reasoning LLM (minimax m2.7 via NVIDIA / gpt-oss-120b via Groq fallback)
"""

import logging

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.llm import reasoning_fallback_llm, reasoning_llm
from app.db.models import Profile, User
from app.services.llm_service import LLMService
from app.services.rag_service import rag_service

logger = logging.getLogger(__name__)

# LLM with failover
llm = LLMService(
    primary=reasoning_llm,
    fallback=reasoning_fallback_llm,
    name="profile_agent",
)


# ──────────────────────────────────────────────
# Structured output schema
# ──────────────────────────────────────────────
class ProfileAnalysis(BaseModel):
    """Structured output from Profile Agent."""
    summary: str = Field(description="Brief summary of the user's career situation (2-3 sentences)")
    strengths: list[str] = Field(description="Key strengths based on current skills and experience")
    skill_gaps: list[str] = Field(description="Skills they need to learn for their target role")
    recommended_focus: str = Field(description="The single most important area to focus on first")
    estimated_gap_months: int = Field(description="Estimated months to reach target role readiness")


# ──────────────────────────────────────────────
# System prompts (bilingual)
# ──────────────────────────────────────────────
SYSTEM_PROMPT_ID = """Kamu adalah Profile Agent untuk Kaix, aplikasi pengembangan karir personal.

Tugasmu:
1. Menganalisis profil pengguna dari data onboarding mereka
2. Mengidentifikasi kekuatan dan kesenjangan skill terhadap target karir mereka
3. Memberikan analisis yang jujur tapi mendukung — realistis tentang kesenjangan, optimis tentang potensi

Selalu jawab dalam Bahasa Indonesia."""

SYSTEM_PROMPT_EN = """You are the Profile Agent for Kaix, a personal career development app.

Your job:
1. Analyze the user's profile from their onboarding data
2. Identify strengths and skill gaps against their target career
3. Provide an honest but supportive analysis — realistic about gaps, optimistic about potential

Always respond in English."""


async def save_profile_data(
    db: AsyncSession,
    user: User,
    onboarding_data: dict,
) -> dict:
    """
    Save onboarding data to the profile (fast, no LLM).
    Returns dict with profile info.
    """
    locale = onboarding_data.get("locale", "id")

    # Upsert profile in DB
    profile = await db.get(Profile, user.id)
    if not profile:
        profile = Profile(user_id=user.id)
        db.add(profile)

    # Map onboarding fields to profile
    profile.current_role = onboarding_data.get("current_role")
    profile.current_field = onboarding_data.get("current_field")
    profile.target_role = onboarding_data.get("target_role")
    profile.target_field = onboarding_data.get("target_field")
    profile.experience_level = onboarding_data.get("experience_level")
    profile.years_experience = onboarding_data.get("years_experience")
    profile.current_skills = onboarding_data.get("current_skills", [])
    profile.time_budget_minutes = onboarding_data.get("time_budget_minutes", 60)
    profile.preferred_learning_style = onboarding_data.get("preferred_learning_style")
    profile.preferred_study_time = onboarding_data.get("preferred_study_time")
    profile.blockers = onboarding_data.get("blockers", [])
    profile.onboarding_completed = True
    profile.gap_score = 0.5  # Default, will be updated by LLM analysis later

    await db.flush()

    # Update user locale
    user.locale = locale
    user.name = onboarding_data.get("name", user.name)
    await db.flush()

    logger.info(f"Profile saved for user={user.id}, target={profile.target_role}")

    return {
        "profile": {
            "user_id": str(user.id),
            "target_role": profile.target_role,
            "experience_level": profile.experience_level,
            "gap_score": profile.gap_score,
            "onboarding_completed": True,
        },
    }


async def run_profile_agent(
    db: AsyncSession,
    user: User,
    onboarding_data: dict,
) -> dict:
    """
    Process onboarding data into a structured profile.

    Steps:
        1. Save raw profile data to DB
        2. Run LLM analysis to extract insights
        3. Compute gap_score (deterministic, not LLM)
        4. Store profile embedding in User RAG

    Returns:
        dict with profile data + analysis
    """
    locale = onboarding_data.get("locale", "id")
    system_prompt = SYSTEM_PROMPT_ID if locale == "id" else SYSTEM_PROMPT_EN

    # 1. Upsert profile in DB
    profile = await db.get(Profile, user.id)
    if not profile:
        profile = Profile(user_id=user.id)
        db.add(profile)

    # Map onboarding fields to profile
    profile.current_role = onboarding_data.get("current_role")
    profile.current_field = onboarding_data.get("current_field")
    profile.target_role = onboarding_data.get("target_role")
    profile.target_field = onboarding_data.get("target_field")
    profile.experience_level = onboarding_data.get("experience_level")
    profile.years_experience = onboarding_data.get("years_experience")
    profile.current_skills = onboarding_data.get("current_skills", [])
    profile.time_budget_minutes = onboarding_data.get("time_budget_minutes", 60)
    profile.preferred_learning_style = onboarding_data.get("preferred_learning_style")
    profile.preferred_study_time = onboarding_data.get("preferred_study_time")
    profile.blockers = onboarding_data.get("blockers", [])
    profile.onboarding_completed = True

    await db.flush()

    # 2. Run LLM analysis
    user_context = f"""
User Profile:
- Name: {user.name}
- Current Role: {profile.current_role or 'None/Student'}
- Current Field: {profile.current_field or 'N/A'}
- Target Role: {profile.target_role}
- Target Field: {profile.target_field or 'Technology'}
- Experience Level: {profile.experience_level}
- Years of Experience: {profile.years_experience}
- Current Skills: {', '.join(profile.current_skills) if profile.current_skills else 'None listed'}
- Time Budget: {profile.time_budget_minutes} minutes/day
- Learning Style: {profile.preferred_learning_style or 'Not specified'}
- Study Time: {profile.preferred_study_time or 'Not specified'}
- Blockers: {', '.join(profile.blockers) if profile.blockers else 'None'}
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Analyze this user's profile and provide your assessment:\n\n{user_context}"),
    ]

    try:
        analysis = await llm.ainvoke_with_structured_output(
            messages, schema=ProfileAnalysis
        )
        profile.profile_json = {
            "summary": analysis.summary,
            "strengths": analysis.strengths,
            "skill_gaps": analysis.skill_gaps,
            "recommended_focus": analysis.recommended_focus,
            "estimated_gap_months": analysis.estimated_gap_months,
        }
        # Use estimated gap months to compute a normalized gap_score (0-1)
        profile.gap_score = min(analysis.estimated_gap_months / 60, 1.0)
    except Exception as e:
        logger.error(f"Profile analysis LLM failed: {e}")
        # Fallback: save profile without AI analysis
        profile.profile_json = {"error": "AI analysis unavailable, will retry"}
        profile.gap_score = 0.5  # Default middle gap

    await db.flush()

    # 3. Embed profile in User RAG for future context
    try:
        profile_text = (
            f"User {user.name} is a {profile.experience_level} "
            f"with {profile.years_experience} years experience. "
            f"Currently: {profile.current_role}. Target: {profile.target_role}. "
            f"Skills: {', '.join(profile.current_skills or [])}. "
            f"Studies {profile.time_budget_minutes} min/day."
        )
        await rag_service.store_user_chunk(
            db=db,
            user_id=user.id,
            content=profile_text,
            metadata={"type": "profile", "version": "onboarding"},
        )
    except Exception as e:
        logger.warning(f"Failed to embed profile in User RAG: {e}")

    # Update user locale
    user.locale = locale
    user.name = onboarding_data.get("name", user.name)
    await db.flush()

    return {
        "profile": {
            "user_id": str(user.id),
            "target_role": profile.target_role,
            "experience_level": profile.experience_level,
            "gap_score": profile.gap_score,
            "onboarding_completed": True,
        },
        "analysis": profile.profile_json,
    }
