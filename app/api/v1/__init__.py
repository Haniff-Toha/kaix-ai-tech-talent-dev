"""
Kaix — API v1 route registrations.
"""

from fastapi import APIRouter

from app.api.v1 import (
    activities,
    auth,
    chat,
    courses,
    notifications,
    onboarding,
    overview,
    recommendations,
    reminders,
    roadmap,
    stats,
    telegram,
)

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router, tags=["Auth"])
router.include_router(onboarding.router, tags=["Onboarding"])
router.include_router(roadmap.router, tags=["Roadmap"])
router.include_router(activities.router, tags=["Activities"])
router.include_router(courses.router, tags=["Learning Hub"])
router.include_router(overview.router, tags=["Overview"])
router.include_router(chat.router, tags=["Chat"])
router.include_router(reminders.router, tags=["Reminders"])
router.include_router(recommendations.router, tags=["Recommendations"])
router.include_router(stats.router, tags=["Stats"])
router.include_router(notifications.router, tags=["Notifications"])
router.include_router(telegram.router, tags=["Telegram"])
