"""Scheduler for daily/weekly reminders"""
from datetime import datetime, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from models.database import get_session, User
import logging

logger = logging.getLogger(__name__)

async def send_daily_reminder(application, user_id, telegram_id, timezone_str):
    """Send daily check-in reminder"""
    try:
        await application.bot.send_message(
            chat_id=telegram_id,
            text=(
                "🌅 *Daily Check-In Reminder*\n\n"
                "Time for your 5-minute daily check-in.\n\n"
                "Use /daily to get started.\n\n"
                "This takes 5 minutes and helps you maintain clarity."
            ),
            parse_mode='Markdown'
        )
        logger.info(f"Sent daily reminder to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send daily reminder to user {user_id}: {e}")

async def send_weekly_reminder(application, user_id, telegram_id):
    """Send weekly review reminder"""
    try:
        await application.bot.send_message(
            chat_id=telegram_id,
            text=(
                "📊 *Weekly Review Reminder*\n\n"
                "End of the week—time for your weekly review.\n\n"
                "Use /weekly to reflect on the past 7 days.\n\n"
                "This takes 20 minutes and helps separate signal from noise."
            ),
            parse_mode='Markdown'
        )
        logger.info(f"Sent weekly reminder to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send weekly reminder to user {user_id}: {e}")

def setup_scheduler(application):
    """Setup APScheduler for reminders"""
    scheduler = AsyncIOScheduler(timezone=pytz.UTC)

    def schedule_user_reminders():
        """Schedule reminders for all users"""
        session = get_session()
        users = session.query(User).filter_by(onboarding_completed=True).all()

        for user in users:
            try:
                # Parse user's reminder time
                time_parts = user.daily_reminder_time.split(':')
                hour = int(time_parts[0])
                minute = int(time_parts[1])

                # Get user timezone
                user_tz = pytz.timezone(user.timezone or 'UTC')

                # Create trigger for daily reminder
                daily_trigger = CronTrigger(
                    hour=hour,
                    minute=minute,
                    timezone=user_tz
                )

                # Schedule daily reminder
                job_id = f"daily_reminder_{user.id}"
                if scheduler.get_job(job_id):
                    scheduler.remove_job(job_id)

                scheduler.add_job(
                    send_daily_reminder,
                    trigger=daily_trigger,
                    args=[application, user.id, user.telegram_id, user.timezone],
                    id=job_id,
                    replace_existing=True
                )

                # Schedule weekly reminder (Friday 5pm in user's timezone)
                weekly_day = 4  # Friday (0 = Monday)
                weekly_trigger = CronTrigger(
                    day_of_week=weekly_day,
                    hour=17,
                    minute=0,
                    timezone=user_tz
                )

                job_id = f"weekly_reminder_{user.id}"
                if scheduler.get_job(job_id):
                    scheduler.remove_job(job_id)

                scheduler.add_job(
                    send_weekly_reminder,
                    trigger=weekly_trigger,
                    args=[application, user.id, user.telegram_id],
                    id=job_id,
                    replace_existing=True
                )

                logger.info(f"Scheduled reminders for user {user.id} (timezone: {user.timezone})")

            except Exception as e:
                logger.error(f"Failed to schedule reminders for user {user.id}: {e}")

        session.close()

    # Schedule reminder setup to run on startup and daily
    scheduler.add_job(schedule_user_reminders, 'interval', hours=24, next_run_time=datetime.now())

    scheduler.start()
    logger.info("Scheduler started")

    return scheduler
