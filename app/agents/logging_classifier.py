"""
Logging Classifier — classifies activity logs against roadmap milestones.

Responsibilities:
    - Parse free-text activity description
    - Map to the most relevant milestone in the user's active roadmap
    - Calculate progress delta (capped at 0.20 per entry)
    - Flag low-confidence classifications for user confirmation
    - Store classification in DB + User RAG

Model: Fast LLM (gemma-3-27b-it via Groq)
"""

import logging

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.llm import fast_llm
from app.db.models import ActivityLog, Roadmap, User
from app.services.llm_service import LLMService
from app.services.rag_service import rag_service
from app.services.streak_service import streak_service

logger = logging.getLogger(__name__)

llm = LLMService(primary=fast_llm, name="logging_classifier")


# ──────────────────────────────────────────────
# Structured output schema
# ──────────────────────────────────────────────
class ActivityClassification(BaseModel):
    """Structured classification result from the Logging Classifier."""
    classified_skill: str = Field(description="The primary skill this activity relates to")
    mapped_milestone_id: str = Field(description="The milestone ID this maps to (e.g. 'm001')")
    mapped_task_id: str | None = Field(
        default=None, description="The specific task ID if identifiable (e.g. 't003')"
    )
    confidence: float = Field(
        ge=0, le=1, description="Classification confidence (0.0-1.0)"
    )
    extracted_topics: list[str] = Field(description="Specific topics mentioned in the activity")
    skill_level_signal: str = Field(
        description="Inferred skill level signal: 'learning', 'practicing', 'applying', 'mastering'"
    )
    milestone_progress_delta: float = Field(
        ge=0, le=0.20, description="Progress increment for the milestone (0.0-0.20)"
    )
    source_type: str = Field(
        description="Activity source type: 'study', 'project', 'course', 'reading', 'practice', 'other'"
    )
    summary: str = Field(description="Brief summary of what the user did (1 sentence)")


# ──────────────────────────────────────────────
# System prompts (bilingual)
# ──────────────────────────────────────────────
SYSTEM_PROMPT_ID = """Kamu adalah Logging Classifier untuk Kaix. Tugasmu mengklasifikasikan aktivitas belajar pengguna terhadap roadmap karir mereka.

Aturan:
1. Cocokkan aktivitas ke milestone yang paling relevan dalam roadmap
2. confidence harus jujur — jika tidak yakin, set di bawah 0.6
3. milestone_progress_delta: 0.03-0.20 tergantung seberapa substantif aktivitasnya
   - Membaca artikel singkat: 0.03-0.05
   - Menyelesaikan tutorial: 0.05-0.10
   - Mengerjakan project: 0.10-0.15
   - Menyelesaikan milestone task: 0.15-0.20
4. Jika aktivitas tidak jelas cocok ke milestone mana, set confidence < 0.6
5. extracted_topics harus spesifik (contoh: "React hooks", "CSS flexbox")

Jawab dalam format yang diminta."""

SYSTEM_PROMPT_EN = """You are the Logging Classifier for Kaix. Your job is to classify user learning activities against their career roadmap.

Rules:
1. Match the activity to the most relevant milestone in the roadmap
2. confidence must be honest — if uncertain, set below 0.6
3. milestone_progress_delta: 0.03-0.20 depending on how substantive the activity is
   - Reading a short article: 0.03-0.05
   - Completing a tutorial: 0.05-0.10
   - Working on a project: 0.10-0.15
   - Completing a milestone task: 0.15-0.20
4. If unclear which milestone, set confidence < 0.6
5. extracted_topics must be specific (e.g. "React hooks", "CSS flexbox")

Respond in the requested format."""


async def run_logging_classifier(
    db: AsyncSession,
    user: User,
    raw_text: str,
    duration_minutes: int | None = None,
) -> dict:
    """
    Classify a free-text activity log against the user's roadmap.

    Steps:
        1. Get active roadmap
        2. Build context with relevant milestones
        3. Run LLM classification
        4. Save ActivityLog to DB
        5. Update streak
        6. Embed in User RAG

    Returns:
        dict with classification result
    """
    locale = user.locale or "id"
    system_prompt = SYSTEM_PROMPT_ID if locale == "id" else SYSTEM_PROMPT_EN

    # 1. Get active roadmap
    result = await db.execute(
        select(Roadmap)
        .where(Roadmap.user_id == user.id, Roadmap.is_active == True)  # noqa: E712
        .order_by(Roadmap.generated_at.desc())
        .limit(1)
    )
    roadmap = result.scalar_one_or_none()

    if not roadmap:
        # No roadmap yet — save as unclassified
        log = ActivityLog(
            user_id=user.id,
            raw_text=raw_text,
            duration_minutes=duration_minutes,
            needs_confirmation=True,
            source_type="other",
        )
        db.add(log)
        await streak_service.update_streak(db, user.id)
        await db.flush()
        return {
            "log_id": str(log.id),
            "classified": False,
            "message": "No active roadmap. Activity logged but not classified.",
        }

    # 2. Extract milestone list from roadmap JSON
    roadmap_data = roadmap.roadmap_json
    milestones_context = []
    for phase in roadmap_data.get("phases", []):
        for ms in phase.get("milestones", []):
            milestones_context.append(
                f"- {ms['milestone_id']}: {ms['title']} — {ms.get('description', '')}"
            )

    milestones_text = "\n".join(milestones_context)

    # 3. Run LLM classification
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""
Classify this activity against the user's roadmap milestones.

ACTIVITY:
"{raw_text}"
{f"Duration: {duration_minutes} minutes" if duration_minutes else ""}

AVAILABLE MILESTONES:
{milestones_text}
"""),
    ]

    try:
        classification = await llm.ainvoke_with_structured_output(
            messages, schema=ActivityClassification
        )
    except Exception as e:
        logger.error(f"Classification failed: {e}")
        # Save as unclassified
        log = ActivityLog(
            user_id=user.id,
            raw_text=raw_text,
            duration_minutes=duration_minutes,
            needs_confirmation=True,
            source_type="other",
        )
        db.add(log)
        await streak_service.update_streak(db, user.id)
        await db.flush()
        return {
            "log_id": str(log.id),
            "classified": False,
            "message": "Classification failed. Activity logged for manual review.",
        }

    # 4. Save ActivityLog
    needs_confirmation = classification.confidence < 0.6
    log = ActivityLog(
        user_id=user.id,
        raw_text=raw_text,
        classified_skill=classification.classified_skill,
        mapped_milestone_id=classification.mapped_milestone_id,
        mapped_task_id=classification.mapped_task_id,
        confidence=classification.confidence,
        duration_minutes=duration_minutes,
        source_type=classification.source_type,
        extracted_topics=classification.extracted_topics,
        skill_level_signal=classification.skill_level_signal,
        milestone_progress_delta=classification.milestone_progress_delta,
        needs_confirmation=needs_confirmation,
        confirmed=not needs_confirmation,
    )
    db.add(log)

    # 5. Update streak
    await streak_service.update_streak(db, user.id)

    await db.flush()

    # 6. Embed in User RAG (fire-and-forget via try/except)
    try:
        rag_text = (
            f"Activity: {raw_text}. "
            f"Skill: {classification.classified_skill}. "
            f"Topics: {', '.join(classification.extracted_topics)}. "
            f"Milestone: {classification.mapped_milestone_id}."
        )
        await rag_service.store_user_chunk(
            db=db,
            user_id=user.id,
            content=rag_text,
            metadata={
                "type": "activity_log",
                "milestone_id": classification.mapped_milestone_id,
                "log_id": str(log.id),
            },
        )
    except Exception as e:
        logger.warning(f"Failed to embed activity in User RAG: {e}")

    return {
        "log_id": str(log.id),
        "classified": True,
        "classification": classification.model_dump(),
        "needs_confirmation": needs_confirmation,
    }
