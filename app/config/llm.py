"""
LLM client configuration.

All LLM providers use OpenAI-compatible endpoints via LangChain's ChatOpenAI.
Embeddings are handled separately in app/services/embedding_service.py
using the google-genai SDK directly (for output_dimensionality control).

Provider overview:
    - Groq        → Reasoning (primary): openai/gpt-oss-120b
    - Groq        → Fast (routing/classification): llama-3.3-70b-versatile
    - Groq        → Vision: meta-llama/llama-4-scout-17b-16e-instruct
    - Google      → Embeddings: gemini-embedding-2-preview (see embedding_service.py)

NOTE: NVIDIA NIM is currently unreachable (timeout). Keeping config but not using as primary.
"""

from langchain_openai import ChatOpenAI

from app.config import settings


# ──────────────────────────────────────────────
# Reasoning LLM — primary (Groq)
# Used by: Profile Agent, Roadmap Agent
# TPM limit: 8000 — keep prompt + max_tokens < 8000
# ──────────────────────────────────────────────
reasoning_llm = ChatOpenAI(
    model=settings.groq_reasoning_model,
    base_url=settings.groq_base_url,
    api_key=settings.groq_api_key,
    temperature=0.4,
    max_tokens=4096,
    timeout=60,
)

# ──────────────────────────────────────────────
# Reasoning LLM — fallback (Groq, smaller model)
# Used when primary model is rate-limited
# ──────────────────────────────────────────────
reasoning_fallback_llm = ChatOpenAI(
    model="llama-3.3-70b-versatile",
    base_url=settings.groq_base_url,
    api_key=settings.groq_api_key,
    temperature=0.4,
    max_tokens=4096,
    timeout=60,
)

# ──────────────────────────────────────────────
# Fast LLM (Groq)
# Used by: Orchestrator routing, Logging Classifier, Nudge Agent
# ──────────────────────────────────────────────
fast_llm = ChatOpenAI(
    model="llama-3.3-70b-versatile",
    base_url=settings.groq_base_url,
    api_key=settings.groq_api_key,
    temperature=0.2,
    max_tokens=2048,
    timeout=30,
)

# ──────────────────────────────────────────────
# Vision LLM (Groq)
# Used by: Verification Agent (Phase 1)
# ──────────────────────────────────────────────
vision_llm = ChatOpenAI(
    model=settings.groq_vision_model,
    base_url=settings.groq_base_url,
    api_key=settings.groq_api_key,
    temperature=0.1,
    max_tokens=1024,
    timeout=30,
)
