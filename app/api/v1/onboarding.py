"""
Onboarding & Profile endpoints.

POST /onboarding  — Submit onboarding form → Save Profile → Roadmap Agent (background)
GET  /profile/me   — Get current user profile
"""

import logging
import traceback

from fastapi import APIRouter, BackgroundTasks

from app.agents.profile_agent import save_profile_data
from app.agents.roadmap_agent import run_roadmap_agent
from app.api.deps import CurrentUser, DBSession
from app.db.models import Job, Profile
from app.db.session import async_session
from app.schemas import (
    APIResponse,
    OnboardingRequest,
    ProfileResponse,
    ProfileUpdateRequest,
)

logger = logging.getLogger(__name__)
router = APIRouter()


async def _generate_roadmap_in_background(user_id, job_id):
    """
    Background task: run Roadmap Agent after profile is saved.
    Uses its own DB session since we're outside the request lifecycle.
    """
    async with async_session() as db:
        try:
            # Update job status
            job = await db.get(Job, job_id)
            if job:
                job.status = "running"
                await db.commit()

            from app.db.models import User

            user = await db.get(User, user_id)
            if not user:
                raise ValueError(f"User {user_id} not found")

            logger.info(f"Starting background roadmap generation for user={user_id}")

            result = await run_roadmap_agent(db=db, user=user)

            # Commit the roadmap + update job as done
            job = await db.get(Job, job_id)
            if job:
                job.status = "done"
                job.result = result
            await db.commit()

            logger.info(f"Background roadmap generation complete for user={user_id}")

        except Exception as e:
            logger.error(
                f"Background roadmap generation failed for user={user_id}: {e}\n"
                f"{traceback.format_exc()}"
            )
            try:
                await db.rollback()
                async with async_session() as err_db:
                    job = await err_db.get(Job, job_id)
                    if job:
                        job.status = "failed"
                        job.error = str(e)[:500]
                        await err_db.commit()
            except Exception as inner_e:
                logger.error(f"Failed to update job status: {inner_e}")


@router.post("/onboarding", response_model=APIResponse)
async def submit_onboarding(
    request: OnboardingRequest,
    background_tasks: BackgroundTasks,
    user: CurrentUser,
    db: DBSession,
):
    """
    Submit onboarding form.

    Flow:
        1. Save profile data immediately (fast, no LLM)
        2. Queue roadmap generation in background
        3. Return immediately with job_id for polling
    """
    # Use the authenticated user's name if not provided
    onboarding_data = request.model_dump()
    if not onboarding_data.get("name"):
        onboarding_data["name"] = user.name or user.email.split("@")[0]

    # Save profile data (fast — no LLM calls)
    profile_result = await save_profile_data(
        db=db,
        user=user,
        onboarding_data=onboarding_data,
    )

    # Create job for background roadmap generation
    job = Job(
        user_id=user.id,
        type="roadmap_generation",
        status="pending",
    )
    db.add(job)
    await db.flush()

    # Commit the profile + job so background task can access them
    await db.commit()

    logger.info(f"Onboarding saved for user={user.id}, queuing roadmap generation job={job.id}")

    # Queue roadmap generation in background
    background_tasks.add_task(
        _generate_roadmap_in_background,
        user_id=user.id,
        job_id=job.id,
    )

    return APIResponse(
        data={
            "profile": profile_result,
            "roadmap_job": {
                "job_id": str(job.id),
                "status": "pending",
                "message": "Roadmap sedang dibuat... / Generating your roadmap...",
            },
        },
        message="Onboarding berhasil! / Onboarding complete!",
    )


@router.get("/profile/me", response_model=APIResponse)
async def get_profile(user: CurrentUser, db: DBSession):
    """Get current user's profile."""
    profile = await db.get(Profile, user.id)
    if not profile:
        return APIResponse(
            data=None,
            message="Profile belum dibuat / Profile not found",
        )

    return APIResponse(
        data=ProfileResponse.model_validate(profile).model_dump(),
        message="Profile loaded",
    )


@router.put("/profile", response_model=APIResponse)
async def update_profile(
    request: ProfileUpdateRequest,
    user: CurrentUser,
    db: DBSession,
):
    """Update current user's profile and name."""
    profile = await db.get(Profile, user.id)
    if not profile:
        return APIResponse(
            success=False,
            data=None,
            message="Profile belum dibuat / Profile not found",
        )

    # Update User name if provided
    if request.name is not None:
        user.name = request.name

    # Update Profile fields if provided
    if request.current_role is not None:
        profile.current_role = request.current_role
    if request.current_field is not None:
        profile.current_field = request.current_field
    if request.target_role is not None:
        profile.target_role = request.target_role
    if request.target_field is not None:
        profile.target_field = request.target_field
    if request.experience_level is not None:
        profile.experience_level = request.experience_level
    if request.years_experience is not None:
        profile.years_experience = request.years_experience
    if request.current_skills is not None:
        profile.current_skills = request.current_skills
    if request.time_budget_minutes is not None:
        profile.time_budget_minutes = request.time_budget_minutes
    if request.preferred_learning_style is not None:
        profile.preferred_learning_style = request.preferred_learning_style
    if request.preferred_study_time is not None:
        profile.preferred_study_time = request.preferred_study_time
    if request.blockers is not None:
        profile.blockers = request.blockers

    await db.flush()
    await db.commit()

    return APIResponse(
        data={
            "user": {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
            },
            "profile": ProfileResponse.model_validate(profile).model_dump(),
        },
        message="Profile berhasil diperbarui! / Profile updated successfully!",
    )

