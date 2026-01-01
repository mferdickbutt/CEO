# CEO Personal Operating System - Telegram Bot

A complete personal productivity system for CEOs, founders, and operators delivered through Telegram.

This bot helps you maintain clarity through daily check-ins, weekly reviews, quarterly evaluations, annual reflection, goal tracking, and pattern recognition—all based on proven frameworks from Dr. Anthony Gustin, Tim Ferriss, Tony Robbins, and Alex Lieberman.

## Features

✅ **Daily Check-Ins** (5 min) - Track energy, wins, friction, priorities
✅ **Weekly Reviews** (20 min) - Separate signal from noise, identify strategic insights
✅ **Quarterly Reviews** (90 min) - Evaluate goals, detect misalignment, course correct
✅ **Annual Reviews** - Deep reflection and pattern recognition
✅ **Goal Tracking** - 1-year, 3-year, and 10-year goal management
✅ **Self-Interview Exercises** - Identity, values, past year, future self
✅ **Framework Library** - Learn from Gustin, Ferriss, Robbins, Lieberman
✅ **Pattern Tracking** - Identify what works and what doesn't
✅ **Automated Reminders** - Daily and weekly prompts in your timezone
✅ **Private & Secure** - All data stored locally, single-user system

## Quick Start

### 1. Create Your Telegram Bot

1. Open Telegram and message [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Choose a name: `CEO Personal OS`
4. Choose a username: `ceo_personal_os_bot` (must end in 'bot')
5. Copy the token you receive (looks like `123456789:ABCdefGhIjKlmNoPQRsTUVwxyZ`)

### 2. Set Up the Bot

**Option A: Run Locally**

```bash
# Clone the repository
git clone <your-repo-url>
cd ceo-personal-os-bot

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your bot token
# TELEGRAM_BOT_TOKEN=your_token_here

# Run the bot
python bot.py
```

**Option B: Deploy to Railway (Recommended)**

1. Create account at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select this repository
4. Add environment variable:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: Your bot token from BotFather
5. Deploy!

**Option C: Deploy to Render**

1. Create account at [render.com](https://render.com)
2. Click "New +" → "Background Worker"
3. Connect your GitHub repository
4. Set:
   - Name: `ceo-personal-os-bot`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
5. Add environment variable:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: Your bot token
6. Create Background Worker!

### 3. Start Using the Bot

1. Find your bot in Telegram (search for the username you chose)
2. Send `/start`
3. Complete the 5-minute onboarding (`/onboarding`)
4. Start your first daily check-in (`/daily`)

That's it! You're now running your personal operating system.

## Available Commands

### Daily Practice
- `/daily` - Daily check-in (5 min)
- `/weekly` - Weekly review (20 min)

### Reviews & Planning
- `/quarterly` - Quarterly review (90 min)
- `/annual` - Annual review (3-4 hours)

### Goal Management
- `/goals` - View and track goals
- `/setgoal` - Set a new goal

### Self-Discovery
- `/interviews` - Access interview exercises
- `/patterns` - View tracked patterns
- `/memory` - See pattern summary

### Learning
- `/frameworks` - Learn about the frameworks
- `/principles` - Review operating principles

### Settings
- `/settings` - Update timezone and reminders
- `/stats` - See your usage statistics
- `/help` - Show all commands

## System Requirements

- Python 3.8+
- SQLite (included)
- Telegram account

## Environment Variables

```bash
# Required
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Optional
DEFAULT_TIMEZONE=America/New_York  # Default: UTC
DATABASE_URL=sqlite:///ceo_personal_os.db  # For custom DB location
```

## Database

The bot uses SQLite by default, creating `ceo_personal_os.db` in the project directory.

To use PostgreSQL instead (for production):

```bash
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Architecture

```
ceo-personal-os-bot/
├── bot.py                 # Main bot entry point
├── models/
│   └── database.py        # Database models (SQLAlchemy)
├── handlers/
│   ├── onboarding.py      # Initial setup flow
│   ├── daily_checkin.py   # Daily check-in conversation
│   ├── weekly_review.py   # Weekly review conversation
│   ├── goals.py           # Goal management
│   └── interviews.py      # Self-interview exercises
├── utils/
│   └── scheduler.py       # Automated reminders
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Frameworks Included

1. **Annual Review (Dr. Anthony Gustin)** - Structured year-end reflection process
2. **Vivid Vision (Tony Robbins / Cameron Herold)** - Future visualization exercise
3. **Ideal Lifestyle Costing (Tim Ferriss)** - Define what "enough" actually costs
4. **Life Map (Alex Lieberman)** - 6-dimension life balance framework

## How It Works

### Daily Flow
1. Bot sends reminder at your chosen time (default: 6pm)
2. You answer 5 quick questions (5 min)
3. Check-in is saved to your database
4. Patterns emerge over time

### Weekly Flow
1. Bot reminds you Friday afternoon
2. You reflect on the week (20 min)
3. Identify what moved the needle vs. noise
4. Set top 3 priorities for next week

### Quarterly Flow
1. Review your weekly reviews
2. Evaluate goal progress
3. Detect misalignment between effort and outcomes
4. Make course corrections

### Annual Flow
1. Complete comprehensive reflection (3-4 hours)
2. Identify positive and negative patterns
3. Review all life dimensions
4. Set intent for the year ahead

## Privacy & Data

- All data is stored locally in your database
- No data is sent to external services (except Telegram)
- This is a single-user system—only you have access
- You can export all data anytime with `/export`

## Support

For issues or questions:
1. Check `/help` in the bot
2. Review this README
3. Check the source code (it's well-commented)

## License

MIT License - See LICENSE file

## Credits

Built on frameworks by:
- Dr. Anthony Gustin (Annual Review)
- Tim Ferriss (Ideal Lifestyle Costing)
- Tony Robbins / Cameron Herold (Vivid Vision)
- Alex Lieberman (Life Map)

Built with:
- [python-telegram-bot](https://python-telegram-bot.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [APScheduler](https://apscheduler.readthedocs.io/)

## Contributing

This is a personal system, but if you have suggestions:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

**Last Updated:** 2025-12-31
**Version:** 1.0.0

## What's Next?

Once your bot is running:
1. Complete `/onboarding` (5 min)
2. Do your first `/daily` check-in
3. Set your goals with `/setgoal`
4. Complete the Identity & Values interview (`/interviews`)
5. Come back daily and build the habit

This system works through consistency, not intensity. **Years over quarters.**
