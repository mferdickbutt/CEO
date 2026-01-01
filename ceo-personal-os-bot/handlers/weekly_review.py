"""Weekly review conversation handler"""
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
from models.database import get_session, User, WeeklyReview

# Conversation states
MOVED_NEEDLE, NOISE, TIME_LEAK, ENERGY_REFLECTION, INSIGHT, ADJUSTMENT, WINS, LOOPS, PRIORITIES, DONE = range(10)

async def weekly_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start weekly review"""
    user = update.effective_user
    session = get_session()
    db_user = session.query(User).filter_by(telegram_id=user.id).first()

    if not db_user or not db_user.onboarding_completed:
        await update.message.reply_text(
            "Please complete /onboarding first."
        )
        session.close()
        return ConversationHandler.END

    session.close()

    await update.message.reply_text(
        "📊 *Weekly Review*\n\n"
        "This takes about 20 minutes. Find a quiet spot.\n\n"
        "Before we start, scan your daily check-ins from this week to remind yourself what happened.\n\n"
        "*Let's begin:*\n\n"
        "*What moved the needle this week?*\n\n"
        "What actually created progress toward your goals?\n\n"
        "Be specific. 'Had productive meetings' is weak. 'Closed 2 new customers, $40k ARR' is useful.",
        parse_mode='Markdown'
    )
    return MOVED_NEEDLE

async def weekly_moved_needle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save what moved the needle"""
    context.user_data['moved_needle'] = update.message.text

    await update.message.reply_text(
        "*What was noise?*\n\n"
        "What consumed time and energy but didn't move anything forward?\n\n"
        "Meetings that could've been emails? Decisions that didn't need to be made yet? Firefighting that could've been prevented?",
        parse_mode='Markdown'
    )
    return NOISE

async def weekly_noise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save noise"""
    context.user_data['noise'] = update.message.text

    await update.message.reply_text(
        "*Where did time leak?*\n\n"
        "Look at your calendar and daily check-ins. Where did time go that you didn't intend?",
        parse_mode='Markdown'
    )
    return TIME_LEAK

async def weekly_time_leak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save time leak"""
    context.user_data['time_leak'] = update.message.text

    await update.message.reply_text(
        "*Energy Reflection*\n\n"
        "First, what was your average energy this week (1-10)?",
        parse_mode='Markdown'
    )
    return ENERGY_REFLECTION

async def weekly_energy_reflection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle energy reflection"""
    try:
        energy = int(update.message.text)
        if not (1 <= energy <= 10):
            raise ValueError
        context.user_data['avg_energy'] = energy
        context.user_data['energy_step'] = 'gave'

        await update.message.reply_text(
            f"Average energy: {energy}/10\n\n"
            "What *gave* you energy this week?",
            parse_mode='Markdown'
        )
    except:
        await update.message.reply_text("Please enter a number between 1 and 10:")
        return ENERGY_REFLECTION

    return ENERGY_REFLECTION

async def weekly_energy_continuation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Continue energy reflection"""
    step = context.user_data.get('energy_step', 'gave')

    if step == 'gave':
        context.user_data['energy_gave'] = update.message.text
        context.user_data['energy_step'] = 'drained'

        await update.message.reply_text(
            "What *drained* you this week?",
            parse_mode='Markdown'
        )
        return ENERGY_REFLECTION

    elif step == 'drained':
        context.user_data['energy_drained'] = update.message.text

        await update.message.reply_text(
            "*One Strategic Insight*\n\n"
            "What did you learn this week about your business, your team, your market, or yourself?\n\n"
            "Not tactics. Strategy. What do you understand now that you didn't understand 7 days ago?",
            parse_mode='Markdown'
        )
        return INSIGHT

async def weekly_insight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save strategic insight"""
    context.user_data['insight'] = update.message.text

    await update.message.reply_text(
        "*One Adjustment for Next Week*\n\n"
        "Based on this week's experience, what will you change, start, stop, or prioritize next week?",
        parse_mode='Markdown'
    )
    return ADJUSTMENT

async def weekly_adjustment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save adjustment"""
    context.user_data['adjustment'] = update.message.text

    await update.message.reply_text(
        "*Wins to Celebrate*\n\n"
        "What went well this week that you want to acknowledge?",
        parse_mode='Markdown'
    )
    return WINS

async def weekly_wins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save wins"""
    context.user_data['wins'] = update.message.text

    await update.message.reply_text(
        "*Open Loops*\n\n"
        "What's unfinished or unresolved that you're carrying into next week?",
        parse_mode='Markdown'
    )
    return LOOPS

async def weekly_loops(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save open loops"""
    context.user_data['loops'] = update.message.text

    await update.message.reply_text(
        "*Top 3 Priorities for Next Week*\n\n"
        "What are the 3 most important things to accomplish next week?\n\n"
        "Write them as a numbered list (one per line):",
        parse_mode='Markdown'
    )
    return PRIORITIES

async def weekly_priorities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save priorities and complete"""
    context.user_data['priorities'] = update.message.text

    # Save to database
    user = update.effective_user
    session = get_session()
    db_user = session.query(User).filter_by(telegram_id=user.id).first()

    week_start = datetime.now() - timedelta(days=datetime.now().weekday())

    review = WeeklyReview(
        user_id=db_user.id,
        week_start=week_start,
        moved_needle=context.user_data.get('moved_needle'),
        noise=context.user_data.get('noise'),
        time_leak=context.user_data.get('time_leak'),
        avg_energy=context.user_data.get('avg_energy'),
        energy_sources=context.user_data.get('energy_gave'),
        energy_drains=context.user_data.get('energy_drained'),
        strategic_insight=context.user_data.get('insight'),
        adjustment=context.user_data.get('adjustment'),
        wins=context.user_data.get('wins'),
        open_loops=context.user_data.get('loops'),
        top_priorities=context.user_data.get('priorities')
    )

    session.add(review)
    session.commit()
    session.close()

    summary = f"""
✅ *Weekly Review Complete*

*Energy:* {context.user_data.get('avg_energy')}/10
*Strategic Insight:* {context.user_data.get('insight')[:150]}{'...' if len(context.user_data.get('insight', '')) > 150 else ''}
*Adjustment Next Week:* {context.user_data.get('adjustment')[:150]}{'...' if len(context.user_data.get('adjustment', '')) > 150 else ''}

*Top 3 Priorities Next Week:*
{context.user_data.get('priorities')}

---
*What's Next?*
• Review this on Friday to see if you hit your priorities
• Use /quarterly at the end of the quarter
• Use /stats to see patterns emerging
    """

    await update.message.reply_text(
        summary,
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardRemove()
    )

    context.user_data.clear()
    return ConversationHandler.END

async def weekly_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel weekly review"""
    await update.message.reply_text(
        "Weekly review cancelled. You can restart with /weekly anytime.",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END

# Create the conversation handler
weekly_review_handler = ConversationHandler(
    entry_points=[CommandHandler('weekly', weekly_start)],
    states={
        MOVED_NEEDLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, weekly_moved_needle)],
        NOISE: [MessageHandler(filters.TEXT & ~filters.COMMAND, weekly_noise)],
        TIME_LEAK: [MessageHandler(filters.TEXT & ~filters.COMMAND, weekly_time_leak)],
        ENERGY_REFLECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c:
            weekly_energy_reflection(u, c) if 'avg_energy' not in c.user_data else weekly_energy_continuation(u, c))],
        INSIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, weekly_insight)],
        ADJUSTMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, weekly_adjustment)],
        WINS: [MessageHandler(filters.TEXT & ~filters.COMMAND, weekly_wins)],
        LOOPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, weekly_loops)],
        PRIORITIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, weekly_priorities)],
    },
    fallbacks=[CommandHandler('cancel', weekly_cancel)],
)
