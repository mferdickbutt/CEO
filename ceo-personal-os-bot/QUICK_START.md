# ⚡ Quick Start - Deploy in 5 Minutes

## 🎯 Goal
Get your CEO Personal OS Telegram bot running on Railway in 5 minutes.

---

## ✅ What You Need (You Already Have This!)

- ✅ Bot Token: your unique token from @BotFather saved securely
- ✅ GitHub repo: `mferdickbutt/CEO`
- ✅ Branch: `claude/ceo-personal-os-GoqXy`

---

## 🚀 5-Minute Deployment

### Step 1: Go to Railway (30 seconds)

1. Open: **https://railway.app**
2. Click **"Login"**
3. Choose **"Login with GitHub"**
4. Authorize Railway

### Step 2: Create New Project (1 minute)

1. Click **"New Project"** (big purple button)
2. Click **"Deploy from GitHub repo"**
3. Select: **`mferdickbutt/CEO`**
4. Railway starts building...

### Step 3: Configure the Service (2 minutes)

**IMPORTANT:** Railway needs to know where the bot code is.

1. Click on your newly created service (shows "ceo-personal-os-bot" or "CEO")
2. Go to **"Settings"** tab
3. Scroll to **"Service Settings"** section
4. Find **"Root Directory"**
5. Enter: `ceo-personal-os-bot`
6. Click **Save** (checkmark icon)

### Step 4: Add Bot Token (1 minute)

1. Stay on your service page
2. Go to **"Variables"** tab
3. Click **"New Variable"**
4. Enter:
   - **Variable name:** `TELEGRAM_BOT_TOKEN`
   - **Value:** your bot token from @BotFather (no spaces/quotes)
5. Click **"Add"**

### Step 5: Deploy! (30 seconds)

1. Railway automatically redeploys with the new settings
2. Go to **"Deployments"** tab
3. Wait for status to show **"Success"** ✅
4. Click on the latest deployment
5. Click **"View Logs"**
6. You should see: `Starting CEO Personal OS Bot...`
7. Then: `Scheduler started`

**🎉 Your bot is live!**

---

## 📱 Test Your Bot (1 minute)

### Step 1: Find Your Bot in Telegram

1. Open Telegram
2. Search for the username you gave @BotFather
   - (The one ending in `_bot`)
3. Click on your bot

### Step 2: Start Conversation

1. Send: `/start`
2. You should receive:

```
👋 Welcome to your CEO Personal Operating System.

This is a private, single-user productivity system designed for founders,
CEOs, and operators who want clarity without complexity.
...
```

### Step 3: Complete Onboarding

1. Send: `/onboarding`
2. Answer the questions:
   - Your name
   - Your role (e.g., "CEO", "Founder")
   - Your company name
   - Your stage of life
   - Your timezone (e.g., "America/New_York")
   - Your daily reminder time (e.g., "18:00")

### Step 4: First Daily Check-in

1. Send: `/daily`
2. Answer the 5 questions (takes 5 minutes)
3. Bot saves your responses and shows your streak

**✅ You're done! Your personal operating system is running.**

---

## 🎯 What to Do Next

### Daily (5 min)
- Bot will remind you at your chosen time
- Send `/daily`
- Answer 5 quick questions
- Build your streak

### Weekly (20 min)
- Friday afternoon or Sunday evening
- Send `/weekly`
- Reflect on the week
- Set priorities for next week

### Monthly
- Review your patterns
- Send `/stats` to see your progress
- Adjust as needed

### Quarterly (90 min)
- Send `/quarterly`
- Deep review of goals
- Course correction

### Annually (3-4 hours)
- Send `/annual`
- Complete annual review
- Set intent for next year

---

## 📊 Available Commands

**Try these:**

- `/help` - See all commands
- `/stats` - View your stats and streak
- `/goals` - View and set goals
- `/setgoal` - Add a new goal
- `/interviews` - Access self-interview exercises
- `/frameworks` - Learn the frameworks
- `/principles` - Review operating principles

---

## ⚠️ Troubleshooting

### Bot doesn't respond to `/start`:

**Check Railway logs:**
1. Go to Railway project
2. Click on your service
3. Click **"Deployments"** tab
4. Click latest deployment
5. Click **"View Logs"**

**Look for:**
- ✅ `Starting CEO Personal OS Bot...`
- ✅ `Scheduler started`
- ❌ Any error messages

**Common fixes:**
1. Verify **Root Directory** is set to `ceo-personal-os-bot`
2. Verify **TELEGRAM_BOT_TOKEN** is correct (no spaces, no quotes)
3. Check deployment status is **"Success"**

### Bot responds but crashes during `/onboarding`:

- This usually means a code error
- Check Railway logs for Python traceback
- File an issue on GitHub

### Reminders don't work:

- Make sure you completed `/onboarding` with your timezone
- Check that Railway service is still running (should show green dot)

---

## 💰 Cost

**Railway free tier:**
- $5 in credits per month
- Your bot uses ~$0.50-1.00/month
- **Plenty of room in free tier**

**No credit card needed for free tier.**

---

## 🔒 Security Note

Keep your bot token private. Store it as the `TELEGRAM_BOT_TOKEN` variable in Railway and regenerate it via @BotFather if it is ever exposed.

---

## ✨ You're All Set!

Your complete personal operating system is now running 24/7 on Railway.

**The bot will:**
- Send you daily reminders
- Send you weekly reminders
- Track all your check-ins
- Identify patterns over time
- Help you maintain clarity

**All you need to do:**
- Respond to daily reminders (5 min/day)
- Do weekly reviews (20 min/week)
- Trust the system

**Years over quarters. Consistency over intensity.**

---

## 📚 Full Documentation

- `README.md` - Complete bot documentation
- `RAILWAY_DEPLOY.md` - Detailed Railway instructions
- Original system: `../ceo-personal-os/README.md`

---

**Need help?** Check Railway logs first. Most issues are:
1. Root directory not set
2. Bot token incorrect
3. Deployment failed

**Ready to start?** Go to https://railway.app and follow the steps above!

🚀
