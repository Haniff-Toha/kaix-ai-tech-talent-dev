"""
Kaix — FastAPI application entry point.

Start with: uvicorn app.main:app --reload
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import router as v1_router
from app.config import settings

# ──────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
# Silence noisy libraries
for noisy in ("hpack", "httpcore", "httpx", "watchfiles", "sqlalchemy.engine.Engine"):
    logging.getLogger(noisy).setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Lifespan
# ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("🚀 Kaix backend starting up...")
    logger.info(f"   Environment: {settings.app_env}")
    logger.info(f"   Reasoning model: {settings.nvidia_model}")
    logger.info(f"   Fast model: {settings.groq_fast_model}")
    logger.info(f"   Embedding model: {settings.gemini_embedding_model}")

    # Start notification scheduler
    from app.services.scheduler import start_scheduler, stop_scheduler
    start_scheduler()

    yield

    # Stop scheduler
    stop_scheduler()
    logger.info("👋 Kaix backend shutting down...")


# ──────────────────────────────────────────────
# App
# ──────────────────────────────────────────────
app = FastAPI(
    title="Kaix API",
    description="Personal Talent Development Roadmap — AI Career Companion",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(v1_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "app": "kaix",
        "version": "0.1.0",
        "environment": settings.app_env,
    }
