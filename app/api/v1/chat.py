"""
Chat endpoint — Orchestrator entry point.

POST /chat — General AI chat (routed by the Orchestrator)

In Phase 0, this is a simplified version that routes to the appropriate agent
based on keyword matching. Full LangGraph orchestrator comes in Phase 0.5.
"""

import logging

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, SystemMessage

from app.api.deps import CurrentUser, DBSession
from app.config.llm import fast_llm
from app.db.models import Profile, Roadmap
from app.schemas import APIResponse, ChatRequest
from app.services.rag_service import rag_service
from sqlalchemy import select

logger = logging.getLogger(__name__)
router = APIRouter()


SYSTEM_PROMPT_ID = """Kamu adalah Kaix, asisten pengembangan karir personal yang ramah dan suportif.

Konteks pengguna:
{user_context}

Panduan:
1. Jawab pertanyaan tentang karir, skill, dan roadmap pengguna
2. Berikan saran yang konkret dan actionable
3. Gunakan informasi dari konteks pengguna untuk personalisasi
4. Tone: ramah, mendukung, tapi jujur
5. Jika ditanya hal di luar bidang pengembangan karir, redirect dengan sopan

Jawab dalam Bahasa Indonesia."""

SYSTEM_PROMPT_EN = """You are Kaix, a friendly and supportive personal career development assistant.

User context:
{user_context}

Guidelines:
1. Answer questions about the user's career, skills, and roadmap
2. Give concrete, actionable advice
3. Use user context for personalization
4. Tone: friendly, supportive, but honest
5. If asked about things outside career development, politely redirect

Respond in English."""


@router.post("/chat")
async def chat(
    request: ChatRequest,
    user: CurrentUser,
    db: DBSession,
):
    """
    General AI chat via the Orchestrator.

    Phase 0 implementation: direct chat with context injection.
    Full LangGraph orchestrator with tool-calling will be wired in Phase 0.5.
    """
    locale = request.locale or user.locale or "id"

    # Build user context
    profile = await db.get(Profile, user.id)
    result = await db.execute(
        select(Roadmap)
        .where(Roadmap.user_id == user.id, Roadmap.is_active == True)  # noqa: E712
        .limit(1)
    )
    roadmap = result.scalar_one_or_none()

    # Get relevant User RAG context
    rag_context = await rag_service.query_user_rag(
        db=db, user_id=user.id, query=request.message, top_k=3
    )
    rag_text = "\n".join([c["content"] for c in rag_context]) if rag_context else "No history yet."

    user_context = f"""
Name: {user.name}
Current Role: {profile.current_role if profile else 'Unknown'}
Target Role: {profile.target_role if profile else 'Unknown'}
Experience: {profile.experience_level if profile else 'Unknown'}
Active Roadmap: {'Yes' if roadmap else 'No'}
Recent Context: {rag_text}
"""

    system_prompt = (SYSTEM_PROMPT_ID if locale == "id" else SYSTEM_PROMPT_EN).format(
        user_context=user_context
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=request.message),
    ]

    # Stream the response
    async def generate():
        async for chunk in fast_llm.astream(messages):
            if chunk.content:
                yield chunk.content

    return StreamingResponse(generate(), media_type="text/plain")
