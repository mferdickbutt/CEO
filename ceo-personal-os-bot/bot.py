"""
CEO Personal Operating System - Telegram Bot
Main bot file with conversation handlers
"""
import os
import logging
from datetime import datetime, time
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv
import pytz

from models.database import init_db, get_session, User, DailyCheckin, WeeklyReview
from handlers.daily_checkin import daily_checkin_handler
from handlers.weekly_review import weekly_review_handler
from handlers.onboarding import onboarding_handler
from handlers.goals import goals_handler
from handlers.interviews import interview_handler, get_interview_callbacks
from handlers.goals import goals_view
from utils.scheduler import setup_scheduler

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize database
db_session = init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - entry point for the bot"""
    user = update.effective_user
    session = get_session()

    # Check if user exists
    db_user = session.query(User).filter_by(telegram_id=user.id).first()

    if not db_user:
        # New user - start onboarding
        db_user = User(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name
        )
        session.add(db_user)
        session.commit()

        await update.message.reply_text(
            "👋 Welcome to your CEO Personal Operating System.\n\n"
            "This bot is a private operating rhythm coach. It keeps you on a daily/weekly "
            "cadence, captures decisions and patterns, and pulls from proven frameworks "
            "so you can think clearly without more tools. Everything stays with you.\n\n"
            "I'll help you with:\n"
            "• Daily check-ins (5 min)\n"
            "• Weekly reviews (20 min)\n"
            "• Quarterly evaluations (90 min)\n"
            "• Annual reflection and planning\n"
            "• Goal tracking and life design\n"
            "• Pattern recognition\n\n"
            "We'll set your context once, then keep you on cadence with the right prompts "
            "at the right time. You can also dive into frameworks like Annual Review, "
            "Vivid Vision, and Founding Principles when you need deeper guidance.\n\n"
            "Use /onboarding to begin (≈5 minutes), or /help to see all commands."
        )
    else:
        if not db_user.onboarding_completed:
            await update.message.reply_text(
                f"Welcome back, {user.first_name}!\n\n"
                "You haven't completed onboarding yet. Use /onboarding to continue."
            )
        else:
            await update.message.reply_text(
                f"Welcome back, {db_user.name or user.first_name}!\n\n"
                "What would you like to do?\n\n"
                "/daily - Daily check-in (5 min)\n"
                "/weekly - Weekly review (20 min)\n"
                "/quarterly - Quarterly review (90 min)\n"
                "/annual - Annual review\n"
                "/goals - View and set goals\n"
                "/interviews - Self-interview exercises\n"
                "/patterns - View your patterns\n"
                "/frameworks - Explore Annual Review, Vivid Vision, Eisenhower Matrix, and other core frameworks\n"
                "/settings - Update preferences\n"
                "/help - See all commands"
            )

    session.close()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message"""
    help_text = """
🎯 *CEO Personal Operating System*

*Daily Practice*
/daily - Daily check-in (5 min)
/weekly - Weekly review (20 min)

*Reviews & Planning*
/quarterly - Quarterly review (90 min)
/annual - Annual review (3-4 hours)

*Goal Management*
/goals - View, set, and track goals
/setgoal - Set a new goal

*Self-Discovery*
/interviews - Access interview exercises
/patterns - View your tracked patterns
/memory - See pattern summary

*Learning*
/frameworks - Explore Annual Review, Vivid Vision, Eisenhower Matrix, and other core frameworks with when-to-use guidance
/principles - Review the operating principles this system is built on (decision rules, focus, and cadence standards)

*Settings & Data*
/settings - Update timezone and reminders
/stats - See your usage statistics
/export - Export all your data

*Getting Started*
/onboarding - Complete initial setup
/help - This message

---
This system is based on frameworks by Dr. Anthony Gustin, Tim Ferriss, Tony Robbins, and Alex Lieberman.

Your data is private and stored locally.
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics"""
    user = update.effective_user
    session = get_session()

    db_user = session.query(User).filter_by(telegram_id=user.id).first()
    if not db_user:
        await update.message.reply_text("Please use /start first to set up your account.")
        session.close()
        return

    daily_count = len(db_user.daily_checkins)
    weekly_count = len(db_user.weekly_reviews)
    quarterly_count = len(db_user.quarterly_reviews)
    annual_count = len(db_user.annual_reviews)
    goals_count = len([g for g in db_user.goals if g.status == 'active'])
    patterns_count = len(db_user.patterns)

    # Calculate current streak (consecutive days with check-ins)
    streak = 0
    if db_user.daily_checkins:
        sorted_checkins = sorted(db_user.daily_checkins, key=lambda x: x.date, reverse=True)
        current_date = datetime.now().date()

        for checkin in sorted_checkins:
            checkin_date = checkin.date.date()
            if (current_date - checkin_date).days == streak:
                streak += 1
            else:
                break

    stats_text = f"""
📊 *Your Statistics*

*Reflection Practice*
Daily check-ins: {daily_count}
Current streak: {streak} days
Weekly reviews: {weekly_count}
Quarterly reviews: {quarterly_count}
Annual reviews: {annual_count}

*Goal & Pattern Tracking*
Active goals: {goals_count}
Tracked patterns: {patterns_count}

*Member Since*
{db_user.created_at.strftime('%B %d, %Y')}

Keep going! Consistency creates clarity.
    """

    await update.message.reply_text(stats_text, parse_mode='Markdown')
    session.close()

async def frameworks_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show frameworks menu"""
    keyboard = [
        [InlineKeyboardButton("📅 Annual Review (Gustin)", callback_data='fw_annual')],
        [InlineKeyboardButton("🎯 Vivid Vision (Robbins)", callback_data='fw_vivid')],
        [InlineKeyboardButton("💰 Ideal Life Costing (Ferriss)", callback_data='fw_costing')],
        [InlineKeyboardButton("🗺️ Life Map (Lieberman)", callback_data='fw_lifemap')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🧠 *Framework Library*\n\n"
        "These proven frameworks sit on top of your North Star, Principles, and Memory files."
        " They give you the exact prompts used in the text system so you can run the same"
        " deep work inside Telegram when you don't have the repo open.\n\n"
        "Select a framework to see: when to use it, the outcome you get, and the steps to run it.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def framework_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle framework button callbacks"""
    query = update.callback_query
    await query.answer()

    frameworks = {
        'fw_annual': {
            'name': 'Annual Review (Dr. Anthony Gustin)',
            'description': 'A half-day, data-backed retrospective that turns the past year into'
                          ' patterns, decisions, and a forward-looking plan.',
            'when_to_use': 'Late December or early January — block 3-4 uninterrupted hours',
            'outcome': [
                'A full scan of wins, failures, and peak/trough experiences',
                'Named positive + negative patterns captured in memory.md',
                'Category ratings across health, relationships, work, finances, meaning, fun',
                'Stop/Start/Continue list and a guiding word for the year',
                'Refreshed Life Map, Vivid Vision, and updated 1/3/10-year goals'
            ],
            'how_to_run': [
                'Collect data from calendar, finances, photos, notes, travel, and health',
                'List what went well and peak experiences (aim for 20+ wins)',
                'List what went poorly and trough experiences with honest specifics',
                'Extract positive/negative patterns and record them in memory.md',
                'Rate each life category 1-10 and note imbalances',
                'Decide what to Stop/Start/Continue and choose a word of the year'
            ]
        },
        'fw_vivid': {
            'name': 'Vivid Vision (Tony Robbins / Cameron Herold)',
            'description': 'A 3-year, present-tense narrative that makes the future vivid enough'
                          ' that your brain starts building the path.',
            'when_to_use': 'Annual review season, major transitions, or any time you feel stuck',
            'outcome': [
                'A sensory-rich story of your life 3 years from now across 3-6 domains',
                'Clear signals for what to say yes/no to as decisions show up',
                'A weekly touchpoint you can read to stay oriented'
            ],
            'how_to_run': [
                'Pick a 3-year date and choose 3-6 domains (work, health, relationships, finances, lifestyle, impact, fun)',
                'Write in first person, present tense with sensory detail',
                'Describe typical days, how you feel, what you have built, and what you no longer do',
                'Review weekly and adjust as your vision evolves'
            ]
        },
        'fw_costing': {
            'name': 'Ideal Lifestyle Costing (Tim Ferriss)',
            'description': 'A 6-12 month lifestyle design exercise that reveals what "enough" really costs so your business decisions match your life goals.',
            'when_to_use': 'During annual planning or before big calls (raise, sell, change roles)',
            'outcome': [
                'Clear picture of your ideal near-term lifestyle instead of vague “someday” goals',
                'A monthly + annual cost table with a 20% buffer',
                'A Target Monthly Income number to anchor decisions'
            ],
            'how_to_run': [
                'Describe your ideal day-to-day 6-12 months out across work, home, relationships, health, travel, learning, fun',
                'Cost each category honestly (housing, food, transport, health, travel, learning, entertainment, savings, giving)',
                'Add 20% buffer, annualize it, then back into your Target Monthly Income',
                'Compare to current reality and decide what to change now'
            ]
        },
        'fw_lifemap': {
            'name': 'Life Map (Alex Lieberman)',
            'description': 'A six-dimension dashboard that catches imbalance early so you don\'t wake up with a great company and an empty life.',
            'when_to_use': 'Quarterly reviews or anytime you feel lopsided between work and everything else',
            'outcome': [
                'Ratings across Career, Relationships, Health, Meaning, Finances, and Fun (total out of 60)',
                'Danger-zone, underdeveloped, and thriving lists to focus your next 90 days',
                'One or two dimension-specific goals with weekly actions'
            ],
            'how_to_run': [
                'Rate each dimension 1-10 with a one-sentence why',
                'Reflect on current state and what a 10/10 looks like for each area',
                'Mark danger zones (1-4) and thriving areas (8-10) to protect',
                'Pick 1-2 dimensions to improve, set one measurable goal each, and define weekly actions'
            ]
        }
    }

    fw = frameworks.get(query.data)
    if fw:
        text = f"*{fw['name']}*\n\n"
        text += f"_{fw['description']}_\n\n"
        text += f"*When to Use:*\n{fw['when_to_use']}\n\n"
        if fw.get('outcome'):
            text += "*What You Get:*\n"
            for item in fw['outcome']:
                text += f"• {item}\n"
            text += "\n"
        text += "*How to Run:*\n"
        for elem in fw['how_to_run']:
            text += f"• {elem}\n"
        text += "\nUse /annual, /quarterly, /goals, or /memory to apply what you learn."

        await query.edit_message_text(text, parse_mode='Markdown')

async def principles_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show operating principles"""
    principles_text = """
⚡ *Operating Principles*

*1. Reflection Creates Leverage*
Spend 1% of your time in structured reflection. It's the highest-leverage activity available.

*2. Energy Is the Constraint*
Track energy, not just time. Optimize for output per unit of energy.

*3. Clarity Is a Competitive Advantage*
Know what you're optimizing for, what you won't do, and where you're avoiding decisions.

*4. Patterns Predict Outcomes*
Your history contains your instruction manual. Track patterns—successes and failures.

*5. Strategy Is Saying No*
Use this system to make better no's, not just better yes's.

*6. You Can't Manage What You Don't Measure*
Measure the smallest number of things that give you the most insight.

*7. Decision Quality > Decision Quantity*
You're paid to make high-quality decisions under uncertainty, not to be busy.

*8. Systems Beat Willpower*
Build the system. Trust the system. Let it carry you when willpower fails.

*9. Simplicity Scales*
If it's not simple, you won't do it. If you don't do it, it doesn't matter.

*10. This Is a Practice*
Progress over perfection. Consistency over intensity. Years over quarters.

Read the full principles in /help or use /daily to start your practice.
    """
    await update.message.reply_text(principles_text, parse_mode='Markdown')

def main():
    """Start the bot"""
    # Get bot token from environment
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("No TELEGRAM_BOT_TOKEN found in environment variables!")
        logger.error("Please set TELEGRAM_BOT_TOKEN in your .env file")
        return

    # Create application
    application = Application.builder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("goals", goals_view))
    application.add_handler(CommandHandler("frameworks", frameworks_menu))
    application.add_handler(CommandHandler("principles", principles_command))
    application.add_handler(CallbackQueryHandler(framework_callback, pattern='^fw_'))

    # Add conversation handlers
    application.add_handler(onboarding_handler)
    application.add_handler(daily_checkin_handler)
    application.add_handler(weekly_review_handler)
    application.add_handler(goals_handler)
    application.add_handler(interview_handler)

    # Add interview callback handlers
    for callback_handler in get_interview_callbacks():
        application.add_handler(callback_handler)

    # Setup reminder scheduler
    setup_scheduler(application)

    # Start the bot
    logger.info("Starting CEO Personal OS Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
