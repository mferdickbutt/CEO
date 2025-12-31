"""Interview exercises handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

async def interviews_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show interviews menu"""
    keyboard = [
        [InlineKeyboardButton("🎭 Identity & Values", callback_data='int_identity')],
        [InlineKeyboardButton("📅 Past Year Reflection", callback_data='int_pastyear')],
        [InlineKeyboardButton("🔮 Future Self Interview", callback_data='int_future')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎤 *Self-Interview Exercises*\n\n"
        "These are guided reflections designed to surface insights you might miss otherwise.\n\n"
        "They're psychologically safe—no judgment, just honest reflection.\n\n"
        "Select an interview to begin:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def interview_identity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Identity & Values interview"""
    query = update.callback_query
    await query.answer()

    text = """
*🎭 Identity & Values Interview*

This interview helps you clarify who you are, what matters to you, and what you stand for.

*Time:* 30-60 minutes
*Environment:* Quiet, uninterrupted

*Key Questions:*

1. Who are you? (Not your title—who are you when you strip away the roles?)

2. How would you describe yourself in three words?

3. What do people misunderstand about you?

4. What are you known for? What do you want to be known for?

5. Who do you admire? Why?

6. What matters most to you? (Name 5-7 core values)

7. Where are you out of alignment with your values?

8. What are your operating principles? (The rules you live by)

9. What is your philosophy on success? On work? On time?

10. What would you regret not doing? What would you regret doing?

---
*How to use this:*
Block time, answer in writing (not just in your head), be honest.

This is your foundation. When you're uncertain, come back to this.

Use /help to continue your practice.
    """

    await query.edit_message_text(text, parse_mode='Markdown')

async def interview_pastyear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Past year reflection interview"""
    query = update.callback_query
    await query.answer()

    text = """
*📅 Past Year Reflection Interview*

A guided retrospective designed to help you reflect deeply on the past year.

*Time:* 60-90 minutes
*When:* Annually (late December or early January)

*Key Questions:*

1. Tell me about the last year. Highlights first. Now the hard part—what didn't go well?

2. What was your biggest win at work? Biggest failure?

3. What consumed the most time and energy? Was it worth it?

4. Where did you avoid making a hard decision?

5. What are you proud of that no one else sees?

6. What gave you energy? What drained you most?

7. What patterns do you notice in how you work? In how you fail?

8. Who were the most important people? Who did you underinvest in?

9. What did you learn this year? About yourself? About leadership?

10. What do you regret? What are you still carrying that you need to let go of?

11. If this year repeated 10 times, would you be satisfied with your life?

12. What do you want to carry forward? What do you want to leave behind?

---
*After completing this interview:*
Transfer key insights to your patterns (use /patterns)
Use this as input for your annual review (/annual)

Use /help to continue.
    """

    await query.edit_message_text(text, parse_mode='Markdown')

async def interview_future(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Future self interview"""
    query = update.callback_query
    await query.answer()

    text = """
*🔮 Future Self Interview*

You're going to interview yourself from the future.

*Setup:* Imagine it's 3 years from now. You've built the life you wanted. Things worked out. You're proud.

Now, from that future version of yourself, answer these questions to your current self.

*Time:* 30-45 minutes

*Key Questions:*

1. Hey [your name], it's you from 3 years in the future. How are you doing?

2. What are you worried about right now that doesn't actually matter?

3. What should you be paying attention to that you're ignoring?

4. What decision are you avoiding that you need to make?

5. Looking back, what was the best decision you made? The hardest decision that turned out right?

6. What did you start doing that changed everything? What did you stop doing that freed up your life?

7. Describe a typical day in your life (my future life).

8. What does your work look like? What do your relationships look like?

9. What do I not understand yet that I will understand in 3 years?

10. What was the turning point?

11. If you could give me one piece of advice, what would it be?

12. What should I start, stop, or change this week?

---
*Why this works:*
Your future self has perspective you don't have yet. Listen to them.

Do this annually or when you're stuck on a major decision.

Use /help to continue your practice.
    """

    await query.edit_message_text(text, parse_mode='Markdown')

# Create handler
interview_handler = CommandHandler('interviews', interviews_menu)

# Add callback handlers to the main bot
def get_interview_callbacks():
    """Return interview callback handlers"""
    return [
        CallbackQueryHandler(interview_identity, pattern='^int_identity$'),
        CallbackQueryHandler(interview_pastyear, pattern='^int_pastyear$'),
        CallbackQueryHandler(interview_future, pattern='^int_future$'),
    ]
