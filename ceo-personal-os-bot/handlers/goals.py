"""Goals management handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
from models.database import get_session, User, Goal

# Conversation states
GOAL_TYPE, CATEGORY, TITLE, DESCRIPTION, WHY, MEASUREMENT = range(6)

async def goals_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View all goals"""
    user = update.effective_user
    session = get_session()
    db_user = session.query(User).filter_by(telegram_id=user.id).first()

    if not db_user:
        await update.message.reply_text("Please use /start first.")
        session.close()
        return

    goals = [g for g in db_user.goals if g.status == 'active']

    if not goals:
        keyboard = [[InlineKeyboardButton("➕ Set Your First Goal", callback_data='setgoal')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "📊 *Your Goals*\n\n"
            "You haven't set any goals yet.\n\n"
            "Goals give you direction. Without them, you're just reacting.\n\n"
            "Ready to set your first goal?",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        session.close()
        return

    # Group by type
    one_year = [g for g in goals if g.goal_type == '1_year']
    three_year = [g for g in goals if g.goal_type == '3_year']
    ten_year = [g for g in goals if g.goal_type == '10_year']

    text = "📊 *Your Goals*\n\n"

    if one_year:
        text += "*1-Year Goals:*\n"
        for g in one_year:
            progress = f" ({g.progress_rating}/10)" if g.progress_rating else ""
            text += f"• {g.title}{progress}\n"
        text += "\n"

    if three_year:
        text += "*3-Year Goals:*\n"
        for g in three_year:
            text += f"• {g.title}\n"
        text += "\n"

    if ten_year:
        text += "*10-Year Vision:*\n"
        for g in ten_year:
            text += f"• {g.title}\n"
        text += "\n"

    keyboard = [[InlineKeyboardButton("➕ Add New Goal", callback_data='setgoal')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text += "---\n"
    text += "Use /setgoal to add more goals.\n"
    text += "Review progress in your quarterly review (/quarterly)."

    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    session.close()

async def setgoal_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start goal setting"""
    # Handle both command and callback
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
    else:
        message = update.message

    keyboard = [
        [InlineKeyboardButton("1-Year Goal", callback_data='goaltype_1_year')],
        [InlineKeyboardButton("3-Year Goal", callback_data='goaltype_3_year')],
        [InlineKeyboardButton("10-Year Vision", callback_data='goaltype_10_year')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text(
        "🎯 *Set a New Goal*\n\n"
        "What timeframe is this goal for?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return GOAL_TYPE

async def setgoal_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save goal type"""
    query = update.callback_query
    await query.answer()

    goal_type = query.data.replace('goaltype_', '')
    context.user_data['goal_type'] = goal_type

    type_name = {"1_year": "1-Year", "3_year": "3-Year", "10_year": "10-Year"}[goal_type]

    keyboard = [
        [InlineKeyboardButton("Career", callback_data='cat_Career')],
        [InlineKeyboardButton("Relationships", callback_data='cat_Relationships')],
        [InlineKeyboardButton("Health", callback_data='cat_Health')],
        [InlineKeyboardButton("Meaning", callback_data='cat_Meaning')],
        [InlineKeyboardButton("Finances", callback_data='cat_Finances')],
        [InlineKeyboardButton("Fun", callback_data='cat_Fun')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"*{type_name} Goal*\n\n"
        "Which life dimension is this goal for?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return CATEGORY

async def setgoal_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save category"""
    query = update.callback_query
    await query.answer()

    category = query.data.replace('cat_', '')
    context.user_data['goal_category'] = category

    await query.edit_message_text(
        f"*{category} Goal*\n\n"
        "What's the goal? (Be specific)\n\n"
        "Example: 'Reach $5M ARR by Dec 2025' or 'Run a half-marathon'",
        parse_mode='Markdown'
    )
    return TITLE

async def setgoal_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save title"""
    context.user_data['goal_title'] = update.message.text

    await update.message.reply_text(
        "*Why does this matter?*\n\n"
        "Why is this goal important to you? How does it connect to your bigger vision?",
        parse_mode='Markdown'
    )
    return WHY

async def setgoal_why(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save why and complete"""
    context.user_data['goal_why'] = update.message.text

    # Save goal
    user = update.effective_user
    session = get_session()
    db_user = session.query(User).filter_by(telegram_id=user.id).first()

    goal = Goal(
        user_id=db_user.id,
        goal_type=context.user_data.get('goal_type'),
        category=context.user_data.get('goal_category'),
        title=context.user_data.get('goal_title'),
        why_matters=context.user_data.get('goal_why'),
        status='active'
    )

    session.add(goal)
    session.commit()
    session.close()

    type_name = {"1_year": "1-Year", "3_year": "3-Year", "10_year": "10-Year"}[context.user_data.get('goal_type')]

    await update.message.reply_text(
        f"✅ *Goal Created*\n\n"
        f"*Type:* {type_name}\n"
        f"*Category:* {context.user_data.get('goal_category')}\n"
        f"*Goal:* {context.user_data.get('goal_title')}\n\n"
        f"Great! I'll remind you to review this in your quarterly check-ins.\n\n"
        f"Use /goals to see all your goals.",
        parse_mode='Markdown'
    )

    context.user_data.clear()
    return ConversationHandler.END

async def setgoal_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel goal setting"""
    await update.message.reply_text("Goal setting cancelled.")
    context.user_data.clear()
    return ConversationHandler.END

# Create handlers
goals_handler = ConversationHandler(
    entry_points=[
        CommandHandler('setgoal', setgoal_start),
        CallbackQueryHandler(setgoal_start, pattern='^setgoal$')
    ],
    states={
        GOAL_TYPE: [CallbackQueryHandler(setgoal_type, pattern='^goaltype_')],
        CATEGORY: [CallbackQueryHandler(setgoal_category, pattern='^cat_')],
        TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, setgoal_title)],
        WHY: [MessageHandler(filters.TEXT & ~filters.COMMAND, setgoal_why)],
    },
    fallbacks=[CommandHandler('cancel', setgoal_cancel)],
)
