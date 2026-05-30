"""
Streak tracking service.

Handles daily streak calculation, updates, and freeze detection.
Rules:
    - Activity logged today → increment streak (if not already counted)
    - No activity yesterday → streak resets to 1
    - Streak freeze: not implemented in Phase 0 (Phase 1)
"""

import logging
from datetime import date, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Streak

logger = logging.getLogger(__name__)


class StreakService:
    """Manages user streak state."""

    async def update_streak(
        self,
        db: AsyncSession,
        user_id,
        activity_date: date | None = None,
    ) -> Streak:
        """
        Update streak after a successful activity log.

        Logic:
            - If last_activity_date is today → no change (already counted)
            - If last_activity_date is yesterday → increment
            - If last_activity_date is older → reset to 1
            - If no streak record → create with streak=1
        """
        today = activity_date or date.today()
        streak = await db.get(Streak, user_id)

        if not streak:
            # First ever activity
            streak = Streak(
                user_id=user_id,
                current_streak=1,
                longest_streak=1,
                last_activity_date=today,
            )
            db.add(streak)
            await db.flush()
            logger.info(f"Created streak for user={user_id}: 1")
            return streak

        if streak.last_activity_date == today:
            # Already logged today, no change
            return streak

        if streak.last_activity_date == today - timedelta(days=1):
            # Consecutive day — increment
            streak.current_streak += 1
        else:
            # Streak broken — reset to 1
            streak.current_streak = 1

        # Update longest streak
        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak

        streak.last_activity_date = today
        await db.flush()

        logger.info(
            f"Streak updated for user={user_id}: "
            f"current={streak.current_streak}, longest={streak.longest_streak}"
        )
        return streak

    async def get_streak(self, db: AsyncSession, user_id) -> Streak | None:
        """Get current streak state for a user."""
        return await db.get(Streak, user_id)


# Singleton instance
streak_service = StreakService()
