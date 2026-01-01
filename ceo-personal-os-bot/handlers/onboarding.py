"""Onboarding conversation handler"""
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
from models.database import get_session, User

# Conversation states
NAME, ROLE, COMPANY, STAGE, TIMEZONE, REMINDER_TIME, COMPLETE = range(7)

async def onboarding_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start onboarding"""
    await update.message.reply_text(
        "🎯 Let's personalize your CEO Personal Operating System.\n\n"
        "This will take about 5 minutes. I'll ask you some basic questions to customize "
        "the system for you.\n\n"
        "First, what's your name?",
        reply_markup=ReplyKeyboardRemove()
    )
    return NAME

async def onboarding_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save name"""
    context.user_data['name'] = update.message.text

    await update.message.reply_text(
        f"Nice to meet you, {update.message.text}!\n\n"
        "What's your current role?\n"
        "(e.g., CEO, Founder, Co-Founder, Operator, Executive)"
    )
    return ROLE

async def onboarding_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save role"""
    context.user_data['role'] = update.message.text

    await update.message.reply_text(
        "What's your company name?\n"
        "(If you're between companies or working on multiple things, just write what feels right)"
    )
    return COMPANY

async def onboarding_company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save company"""
    context.user_data['company'] = update.message.text

    await update.message.reply_text(
        "What stage of life/work are you in right now?\n\n"
        "Examples:\n"
        "• First-time founder, year 2\n"
        "• Scaling CEO, Series A stage\n"
        "• Second-time founder, pre-launch\n"
        "• Operator transitioning to CEO\n"
        "• Executive exploring what's next\n\n"
        "Your answer:"
    )
    return STAGE

async def onboarding_stage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save stage"""
    context.user_data['stage'] = update.message.text

    timezone_keyboard = [
        ['America/New_York', 'America/Chicago'],
        ['America/Denver', 'America/Los_Angeles'],
        ['Europe/London', 'Europe/Paris'],
        ['Asia/Tokyo', 'Asia/Singapore'],
        ["UTC (I'll set it later)"]
    ]

    await update.message.reply_text(
        "What's your timezone?\n"
        "This helps me send reminders at the right time.",
        reply_markup=ReplyKeyboardMarkup(timezone_keyboard, one_time_keyboard=True)
    )
    return TIMEZONE

async def onboarding_timezone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save timezone"""
    tz = update.message.text
    if tz == 'UTC (I\'ll set it later)':
        tz = 'UTC'
    context.user_data['timezone'] = tz

    await update.message.reply_text(
        "What time should I send daily check-in reminders?\n\n"
        "Format: HH:MM in 24-hour time (e.g., 18:00 for 6pm)\n"
        "Tip: End of workday works well for most people.",
        reply_markup=ReplyKeyboardRemove()
    )
    return REMINDER_TIME

async def onboarding_reminder_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save reminder time and complete onboarding"""
    time_text = update.message.text

    # Validate time format
    try:
        time_parts = time_text.split(':')
        if len(time_parts) != 2:
            raise ValueError
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        if not (0 <= hour < 24 and 0 <= minute < 60):
            raise ValueError
        context.user_data['reminder_time'] = time_text
    except:
        await update.message.reply_text(
            "Please use HH:MM format (e.g., 18:00)"
        )
        return REMINDER_TIME

    # Save to database
    user = update.effective_user
    session = get_session()
    db_user = session.query(User).filter_by(telegram_id=user.id).first()

    if db_user:
        db_user.name = context.user_data.get('name')
        db_user.role = context.user_data.get('role')
        db_user.company = context.user_data.get('company')
        db_user.stage_of_life = context.user_data.get('stage')
        db_user.timezone = context.user_data.get('timezone')
        db_user.daily_reminder_time = context.user_data.get('reminder_time')
        db_user.onboarding_completed = True
        session.commit()

    session.close()

    await update.message.reply_text(
        "✅ Setup complete!\n\n"
        f"Here's your context:\n"
        f"• Name: {context.user_data.get('name')}\n"
        f"• Role: {context.user_data.get('role')}\n"
        f"• Company: {context.user_data.get('company')}\n"
        f"• Stage: {context.user_data.get('stage')}\n"
        f"• Timezone: {context.user_data.get('timezone')}\n"
        f"• Daily reminder: {context.user_data.get('reminder_time')}\n\n"
        "I'll send you a daily reminder at that time for your 5-minute check-in.\n\n"
        "Ready to get started?\n\n"
        "*What to do now:*\n"
        "• /daily - Start your first daily check-in (5 min)\n"
        "• /interviews - Complete the Identity & Values interview (30 min)\n"
        "• /goals - Set your 1-year goals\n"
        "• /frameworks - Learn about the frameworks\n\n"
        "I recommend starting with /daily to get a feel for the system.",
        parse_mode='Markdown'
    )

    return ConversationHandler.END

async def onboarding_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel onboarding"""
    await update.message.reply_text(
        "Onboarding cancelled. You can restart anytime with /onboarding",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Create the conversation handler
onboarding_handler = ConversationHandler(
    entry_points=[CommandHandler('onboarding', onboarding_start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, onboarding_name)],
        ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, onboarding_role)],
        COMPANY: [MessageHandler(filters.TEXT & ~filters.COMMAND, onboarding_company)],
        STAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, onboarding_stage)],
        TIMEZONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, onboarding_timezone)],
        REMINDER_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, onboarding_reminder_time)],
    },
    fallbacks=[CommandHandler('cancel', onboarding_cancel)],
)
