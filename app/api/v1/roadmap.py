"""
Roadmap endpoints.

GET  /roadmap          — Get active roadmap
POST /roadmap/regenerate — Regenerate roadmap (background)
"""

import logging

from fastapi import APIRouter, BackgroundTasks

from app.api.deps import CurrentUser, DBSession
from app.db.models import Job, Roadmap
from app.schemas import APIResponse, RoadmapResponse
from sqlalchemy import select

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/roadmap", response_model=APIResponse)
async def get_roadmap(user: CurrentUser, db: DBSession):
    """Get the user's current active roadmap."""
    result = await db.execute(
        select(Roadmap)
        .where(Roadmap.user_id == user.id, Roadmap.is_active == True)  # noqa: E712
        .order_by(Roadmap.generated_at.desc())
        .limit(1)
    )
    roadmap = result.scalar_one_or_none()

    if not roadmap:
        return APIResponse(
            data=None,
            message="Belum ada roadmap. Selesaikan onboarding dulu. / No roadmap yet. Complete onboarding first.",
        )

    return APIResponse(
        data=RoadmapResponse.model_validate(roadmap).model_dump(mode="json"),
    )


@router.post("/roadmap/regenerate", response_model=APIResponse)
async def regenerate_roadmap(
    background_tasks: BackgroundTasks,
    user: CurrentUser,
    db: DBSession,
):
    """Regenerate the user's roadmap in the background."""
    from app.api.v1.onboarding import _generate_roadmap_in_background

    job = Job(user_id=user.id, type="roadmap_regeneration", status="pending")
    db.add(job)
    await db.flush()

    background_tasks.add_task(
        _generate_roadmap_in_background,
        user_id=user.id,
        job_id=job.id,
    )

    return APIResponse(
        data={"job_id": str(job.id), "status": "pending"},
        message="Roadmap sedang dibuat ulang... / Regenerating roadmap...",
    )
