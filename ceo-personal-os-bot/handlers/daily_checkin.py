"""Daily check-in conversation handler"""
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
from models.database import get_session, User, DailyCheckin

# Conversation states
ENERGY, WIN, FRICTION, LET_GO, PRIORITY, NOTES = range(6)

async def daily_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start daily check-in"""
    user = update.effective_user
    session = get_session()
    db_user = session.query(User).filter_by(telegram_id=user.id).first()

    if not db_user or not db_user.onboarding_completed:
        await update.message.reply_text(
            "Please complete /onboarding first to set up your account."
        )
        session.close()
        return ConversationHandler.END

    # Check if already done today
    today = datetime.now().date()
    existing_checkin = next(
        (c for c in db_user.daily_checkins if c.date.date() == today),
        None
    )

    if existing_checkin:
        await update.message.reply_text(
            f"You've already completed your daily check-in today!\n\n"
            f"Energy: {existing_checkin.energy_level}/10\n"
            f"Win: {existing_checkin.meaningful_win}\n\n"
            f"Come back tomorrow, or use /weekly for your weekly review."
        )
        session.close()
        return ConversationHandler.END

    session.close()

    await update.message.reply_text(
        "📝 *Daily Check-In*\n\n"
        "This takes 5 minutes. Just answer honestly—this is for you, not anyone else.\n\n"
        "Let's start:\n\n"
        "*Energy Level*\n"
        "On a scale of 1-10, what was your energy today?\n\n"
        "1 = Completely depleted\n"
        "10 = Fully energized\n\n"
        "Your number:",
        parse_mode='Markdown'
    )
    return ENERGY

async def daily_energy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save energy level"""
    try:
        energy = int(update.message.text)
        if not (1 <= energy <= 10):
            raise ValueError
        context.user_data['daily_energy'] = energy
    except:
        await update.message.reply_text(
            "Please enter a number between 1 and 10:"
        )
        return ENERGY

    await update.message.reply_text(
        "*One Meaningful Win*\n\n"
        "What actually moved the needle today?\n\n"
        "Not busywork—what mattered? What created progress?\n\n"
        "(If nothing, that's fine. Just write 'Nothing today' and we'll move on.)",
        parse_mode='Markdown'
    )
    return WIN

async def daily_win(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save meaningful win"""
    context.user_data['daily_win'] = update.message.text

    await update.message.reply_text(
        "*One Friction Point*\n\n"
        "What drained energy, created frustration, or slowed you down today?\n\n"
        "Be specific. 'Bad meetings' is weak. 'Three status meetings that should have been emails' is useful.",
        parse_mode='Markdown'
    )
    return FRICTION

async def daily_friction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save friction point"""
    context.user_data['daily_friction'] = update.message.text

    await update.message.reply_text(
        "*One Thing to Let Go Of*\n\n"
        "What happened today that you need to release?\n\n"
        "A mistake? A conflict? A missed opportunity? A worry?\n\n"
        "Name it, then let it go.",
        parse_mode='Markdown'
    )
    return LET_GO

async def daily_let_go(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save let go item"""
    context.user_data['daily_let_go'] = update.message.text

    await update.message.reply_text(
        "*One Priority for Tomorrow*\n\n"
        "If you could only accomplish ONE thing tomorrow, what would it be?\n\n"
        "Not a list. One thing that matters.",
        parse_mode='Markdown'
    )
    return PRIORITY

async def daily_priority(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save priority"""
    context.user_data['daily_priority'] = update.message.text

    keyboard = [
        ['Done - Save check-in'],
        ['Add optional notes']
    ]

    await update.message.reply_text(
        "Almost done!\n\n"
        "Do you want to add any optional notes, or are we good?",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    return NOTES

async def daily_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle notes or completion"""
    text = update.message.text

    if text == 'Done - Save check-in':
        context.user_data['daily_notes'] = None
        return await daily_complete(update, context)
    elif text == 'Add optional notes':
        await update.message.reply_text(
            "Add your notes (anything else worth capturing):",
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data['awaiting_notes'] = True
        return NOTES
    elif context.user_data.get('awaiting_notes'):
        context.user_data['daily_notes'] = update.message.text
        return await daily_complete(update, context)
    else:
        return await daily_complete(update, context)

async def daily_complete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Complete daily check-in"""
    user = update.effective_user
    session = get_session()
    db_user = session.query(User).filter_by(telegram_id=user.id).first()

    # Create daily check-in
    checkin = DailyCheckin(
        user_id=db_user.id,
        date=datetime.now(),
        energy_level=context.user_data.get('daily_energy'),
        meaningful_win=context.user_data.get('daily_win'),
        friction_point=context.user_data.get('daily_friction'),
        let_go=context.user_data.get('daily_let_go'),
        priority_tomorrow=context.user_data.get('daily_priority'),
        notes=context.user_data.get('daily_notes')
    )

    session.add(checkin)
    session.commit()

    # Calculate streak
    checkins = sorted(db_user.daily_checkins, key=lambda x: x.date, reverse=True)
    streak = 1
    current_date = datetime.now().date()
    for i, c in enumerate(checkins):
        if i == 0:
            continue
        checkin_date = c.date.date()
        expected_date = (current_date - (i * 1)).days
        if (current_date - checkin_date).days == i:
            streak += 1
        else:
            break

    session.close()

    summary = f"""
✅ *Daily Check-In Complete*

*Your Snapshot:*
Energy: {context.user_data.get('daily_energy')}/10
Win: {context.user_data.get('daily_win')[:100]}{'...' if len(context.user_data.get('daily_win')) > 100 else ''}
Priority Tomorrow: {context.user_data.get('daily_priority')[:100]}{'...' if len(context.user_data.get('daily_priority')) > 100 else ''}

🔥 Current streak: {streak} day{'s' if streak != 1 else ''}

That's it. Close the app. Tomorrow is a new day.

---
*What's Next?*
• Come back tomorrow for another check-in
• Use /weekly on Friday or Sunday for your weekly review
• Use /stats to see your progress
    """

    await update.message.reply_text(
        summary,
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardRemove()
    )

    # Clear context
    context.user_data.clear()

    return ConversationHandler.END

async def daily_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel daily check-in"""
    await update.message.reply_text(
        "Daily check-in cancelled. No problem—try again when you're ready with /daily",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END

# Create the conversation handler
daily_checkin_handler = ConversationHandler(
    entry_points=[CommandHandler('daily', daily_start)],
    states={
        ENERGY: [MessageHandler(filters.TEXT & ~filters.COMMAND, daily_energy)],
        WIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, daily_win)],
        FRICTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, daily_friction)],
        LET_GO: [MessageHandler(filters.TEXT & ~filters.COMMAND, daily_let_go)],
        PRIORITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, daily_priority)],
        NOTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, daily_notes)],
    },
    fallbacks=[CommandHandler('cancel', daily_cancel)],
)
