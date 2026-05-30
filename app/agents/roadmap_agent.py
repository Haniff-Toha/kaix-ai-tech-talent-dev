"""
Roadmap Agent — generates a structured career roadmap.

Uses RAG + SQL data as context, then LLM generates a JSON roadmap.
"""

import json
import logging

from langchain_core.messages import HumanMessage, SystemMessage
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.llm import reasoning_fallback_llm, reasoning_llm
from app.db.models import Profile, Roadmap, ScrapedCourse, User
from app.services.llm_service import LLMService
from app.services.rag_service import rag_service

logger = logging.getLogger(__name__)

# LLM with failover
llm = LLMService(
    primary=reasoning_llm,
    fallback=reasoning_fallback_llm,
    name="roadmap_agent",
)


# ──────────────────────────────────────────────
# System prompt (compact, bilingual)
# ──────────────────────────────────────────────
SYSTEM_PROMPT = """You are a career roadmap generator for Kaix, an AI Tech Talent Companion app.

Generate a JSON career roadmap based on the user profile and knowledge provided.

Output ONLY valid JSON with this exact structure:
{
  "total_phases": 3,
  "estimated_months": 6,
  "daily_quote": "Inspirational quote here",
  "phases": [
    {
      "phase_number": 1,
      "phase_title": "Phase title",
      "description": "What this phase covers",
      "duration_weeks": 4,
      "milestones": [
        {
          "milestone_id": "m001",
          "title": "Milestone title",
          "description": "What to learn",
          "skills": ["skill1", "skill2"],
          "duration_weeks": 2,
          "daily_tasks": [
            {
              "task_id": "t001",
              "title": "Task title",
              "description": "What to do",
              "estimated_minutes": 30,
              "type": "reading"
            }
          ]
        }
      ]
    }
  ]
}

Rules:
- 3-4 phases, 2-3 milestones per phase, 3-5 tasks per milestone
- Task types: reading, coding, project, quiz, video
- Adjust durations to user's daily study time
- Use the Knowledge Base and Available Courses as references
- Output in Bahasa Indonesia (technical terms in English)
- Return ONLY the JSON, no markdown, no explanation"""


async def _get_relevant_courses(
    db: AsyncSession,
    target_role: str,
    limit: int = 8,
) -> list[dict]:
    """Query scraped_courses for the target career track."""
    target_lower = target_role.lower().replace(" ", "_")

    result = await db.execute(
        select(ScrapedCourse)
        .where(
            ScrapedCourse.career_tracks.any(target_lower),
            ScrapedCourse.title.notlike("Rp%"),
        )
        .order_by(
            ScrapedCourse.rating.desc().nullslast(),
            ScrapedCourse.is_free.desc(),
        )
        .limit(limit)
    )
    courses = result.scalars().all()

    if not courses:
        role_keywords = target_role.lower().split("_")
        for keyword in role_keywords:
            if len(keyword) > 3:
                result = await db.execute(
                    select(ScrapedCourse)
                    .where(
                        ScrapedCourse.title.notlike("Rp%"),
                        ScrapedCourse.skills_covered.any(keyword),
                    )
                    .order_by(ScrapedCourse.rating.desc().nullslast())
                    .limit(limit)
                )
                courses = result.scalars().all()
                if courses:
                    break

    return [
        {
            "title": c.title,
            "platform": c.platform_display or c.source,
            "level": c.level,
            "is_free": c.is_free,
        }
        for c in courses
    ]


def _parse_roadmap_json(content: str) -> dict:
    """Extract and parse JSON from LLM response, handling markdown fences."""
    text = content.strip()
    # Remove markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]
    text = text.strip()
    return json.loads(text)


async def run_roadmap_agent(
    db: AsyncSession,
    user: User,
) -> dict:
    """
    Generate a personalized career roadmap using RAG + SQL + LLM.

    Steps:
        1. Load user profile
        2. Query Knowledge RAG for career content
        3. Query scraped_courses for real course data
        4. Generate roadmap via LLM (JSON output)
        5. Save to DB
    """
    # 1. Load profile
    profile = await db.get(Profile, user.id)
    if not profile:
        raise ValueError("User has no profile. Complete onboarding first.")

    target_role = profile.target_role or "software engineer"

    # 2. Query Knowledge RAG
    logger.info(f"Querying Knowledge RAG for target_role={target_role}")
    rag_chunks = await rag_service.query_knowledge_rag(
        db=db,
        query=f"career path skills for {target_role}",
        career_track=target_role,
        top_k=3,
    )

    rag_context = ""
    if rag_chunks:
        rag_context = "\n".join([
            chunk['content'][:400] for chunk in rag_chunks
        ])
        logger.info(f"Got {len(rag_chunks)} RAG chunks for {target_role}")
    else:
        logger.warning(f"No RAG chunks found for {target_role}")

    # 3. Query courses
    logger.info(f"Querying scraped courses for {target_role}")
    courses = await _get_relevant_courses(db, target_role, limit=6)
    courses_text = ""
    if courses:
        courses_text = "\n".join([
            f"- {c['title']} ({c['platform']}, {c['level']}, {'Free' if c['is_free'] else 'Paid'})"
            for c in courses
        ])
        logger.info(f"Got {len(courses)} courses for {target_role}")

    # 4. Build compact prompt
    user_prompt = f"""User: {user.name}
Target: {target_role}
Experience: {profile.experience_level}, {profile.years_experience} years
Skills: {', '.join(profile.current_skills or []) or 'None'}
Daily study: {profile.time_budget_minutes} minutes

Knowledge Base:
{rag_context or 'No specific data.'}

Available Courses:
{courses_text or 'No specific courses.'}

Generate a personalized roadmap JSON for this user."""

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_prompt),
    ]

    # 5. Generate
    logger.info(f"Starting roadmap LLM generation for user={user.id}")
    try:
        response = await llm.ainvoke(messages)
        roadmap_data = _parse_roadmap_json(response.content)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse roadmap JSON: {e}\nContent: {response.content[:500]}")
        raise ValueError(f"LLM returned invalid JSON: {e}")
    except Exception as e:
        logger.error(f"Roadmap generation LLM failed: {e}")
        raise

    logger.info(f"Roadmap LLM generation complete for user={user.id}")

    # 6. Deactivate old roadmaps
    await db.execute(
        update(Roadmap)
        .where(Roadmap.user_id == user.id, Roadmap.is_active == True)  # noqa: E712
        .values(is_active=False)
    )

    # 7. Save new roadmap
    roadmap = Roadmap(
        user_id=user.id,
        target_role=profile.target_role,
        total_phases=roadmap_data.get("total_phases", len(roadmap_data.get("phases", []))),
        estimated_months=roadmap_data.get("estimated_months", 6),
        roadmap_json=roadmap_data,
        is_active=True,
    )
    db.add(roadmap)
    await db.flush()

    logger.info(
        f"Saved roadmap for user={user.id}: "
        f"{roadmap_data.get('total_phases')} phases, "
        f"{roadmap_data.get('estimated_months')} months"
    )

    return {
        "roadmap_id": str(roadmap.id),
        "target_role": profile.target_role,
        "total_phases": roadmap_data.get("total_phases"),
        "estimated_months": roadmap_data.get("estimated_months"),
        "daily_quote": roadmap_data.get("daily_quote", ""),
        "roadmap": roadmap_data,
    }
