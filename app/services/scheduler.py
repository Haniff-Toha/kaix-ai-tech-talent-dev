"""
Scheduler — APScheduler-based background job runner.

Checks for due reminders every minute (at :00 seconds) and dispatches notifications.
Uses CronTrigger for precise minute alignment with explicit Asia/Jakarta timezone.
"""

import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import select

from app.agents.nudge_agent import generate_nudge
from app.db.models import Course, Reminder, User
from app.db.session import async_session as async_session_factory
from app.services.notification_service import dispatch_notification

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()
JAKARTA_TZ = ZoneInfo("Asia/Jakarta")

# Day name mapping (Reminder stores Indonesian day names)
DAY_MAP = {
    0: "Senin",   # Monday
    1: "Selasa",  # Tuesday
    2: "Rabu",    # Wednesday
    3: "Kamis",   # Thursday
    4: "Jumat",   # Friday
    5: "Sabtu",   # Saturday
    6: "Minggu",  # Sunday
}


async def check_due_reminders():
    """
    Check for reminders that are due at the current minute and dispatch.
    Fires at the top of every minute via CronTrigger(second=0).
    Uses explicit Asia/Jakarta timezone for time comparison.
    """
    now = datetime.now(JAKARTA_TZ)
    current_hour = now.hour
    current_minute = now.minute
    current_day = DAY_MAP.get(now.weekday(), "")

    logger.info(f"⏰ Scheduler tick: {current_hour:02d}:{current_minute:02d} ({current_day}) [Jakarta]")

    async with async_session_factory() as db:
        try:
            # Find active reminders matching current time and day
            result = await db.execute(
                select(Reminder).where(
                    Reminder.is_active == True,  # noqa: E712
                )
            )
            reminders = result.scalars().all()

            for reminder in reminders:
                # Check time match (hour and minute)
                if (
                    reminder.scheduled_time.hour != current_hour
                    or reminder.scheduled_time.minute != current_minute
                ):
                    continue

                # Check day match
                if current_day not in (reminder.days or []):
                    continue

                # Avoid sending more than once per scheduled slot
                # Use naive comparison (strip tz from now for comparison)
                if reminder.last_sent_at:
                    now_naive = now.replace(tzinfo=None)
                    diff = (now_naive - reminder.last_sent_at).total_seconds()
                    if diff < 300:  # skip if sent less than 5 minutes ago
                        logger.debug(f"⏭ Skipping reminder '{reminder.label}' — sent {diff:.0f}s ago")
                        continue

                # Get user
                user = await db.get(User, reminder.user_id)
                if not user:
                    continue

                # Build rich context from reminder metadata
                context = {
                    "type": reminder.type,
                    "label": reminder.label,
                    "course_title": None,
                    "course_url": None,
                }

                # Resolve linked course title if present
                if reminder.linked_course_id:
                    course = await db.get(Course, reminder.linked_course_id)
                    if course:
                        context["course_title"] = course.title
                        context["course_url"] = course.url

                logger.info(
                    f"📤 Dispatching reminder '{reminder.label or reminder.type}' "
                    f"to {user.name} via {reminder.channel} at {current_hour:02d}:{current_minute:02d}"
                )

                # Generate nudge message
                nudge = await generate_nudge(db=db, user=user, nudge_type=reminder.type)

                # Dispatch to channel with context
                await dispatch_notification(
                    db=db,
                    user=user,
                    channel=reminder.channel,
                    nudge=nudge,
                    reminder_id=reminder.id,
                    context=context,
                )

                # Update last_sent_at (naive for DB compatibility)
                reminder.last_sent_at = now.replace(tzinfo=None)
                await db.flush()

            await db.commit()
        except Exception as e:
            logger.error(f"Scheduler error: {e}", exc_info=True)
            await db.rollback()


async def run_daily_scraping():
    """
    Background job to run the course scraper and RAG ingest daily.
    Invokes the master scrape_and_ingest script's main entry point.
    """
    logger.info("⏳ Starting daily scheduled course scraping...")
    try:
        from scripts.scrape_and_ingest import main as scrape_and_ingest_main
        # Run default scrape (Dicoding, YouTube, Books, rubythalib)
        await scrape_and_ingest_main()
        logger.info("✅ Daily scheduled course scraping completed successfully.")
    except Exception as e:
        logger.error(f"❌ Daily scheduled course scraping failed: {e}", exc_info=True)


def start_scheduler():
    """Start the APScheduler with the reminder check job."""
    scheduler.add_job(
        check_due_reminders,
        trigger=CronTrigger(second=0, timezone=JAKARTA_TZ),
        id="check_due_reminders",
        name="Check due reminders",
        replace_existing=True,
    )
    scheduler.add_job(
        run_daily_scraping,
        trigger=CronTrigger(hour=2, minute=0, second=0, timezone=JAKARTA_TZ),
        id="run_daily_scraping",
        name="Daily course scraper and ingest",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("🗓️ Notification & Scraper scheduler started (CronTrigger, Asia/Jakarta, check_due_reminders every minute, run_daily_scraping daily at 02:00)")


def stop_scheduler():
    """Gracefully shut down the scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("🗓️ Notification scheduler stopped")
