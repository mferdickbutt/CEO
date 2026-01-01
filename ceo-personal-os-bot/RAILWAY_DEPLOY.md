# 🚀 Railway Deployment Guide

## Your Bot is Ready to Deploy!

**Bot Token:** `8590281913:AAG6VwGKy6iGj3mrQvksGHevPji8sRlI_L8`

---

## Step-by-Step Deployment to Railway

### 1. Push Your Code to GitHub (Already Done ✅)

Your bot is already in the repository at:
- **Branch:** `claude/ceo-personal-os-GoqXy`
- **Directory:** `ceo-personal-os-bot/`

### 2. Deploy to Railway

**Option A: Deploy from GitHub (Recommended)**

1. Go to **https://railway.app**

2. Click **"Login"** → Sign in with GitHub

3. Click **"New Project"**

4. Select **"Deploy from GitHub repo"**

5. Choose your repository: **`mferdickbutt/CEO`**

6. Railway will ask which service to deploy:
   - Select **"Add variables"** or **"Configure"**

7. **CRITICAL:** Set the root directory:
   - Click on your service
   - Go to **Settings** tab
   - Under **"Service"** section, find **"Root Directory"**
   - Set to: `ceo-personal-os-bot`
   - Click **Save**

8. Add your environment variable:
   - Go to **Variables** tab
   - Click **"New Variable"**
   - Add:
     - **Variable:** `TELEGRAM_BOT_TOKEN`
     - **Value:** `8590281913:AAG6VwGKy6iGj3mrQvksGHevPji8sRlI_L8`
   - Click **Add**

9. Railway will automatically:
   - Detect Python
   - Install dependencies from `requirements.txt`
   - Run `python bot.py`
   - Start your bot! 🎉

10. Check the **Logs** to confirm it's running:
    - You should see: `"Starting CEO Personal OS Bot..."`

**Option B: Railway CLI (Advanced)**

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Navigate to bot directory
cd ceo-personal-os-bot

# Initialize Railway project
railway init

# Add environment variable
railway variables set TELEGRAM_BOT_TOKEN=8590281913:AAG6VwGKy6iGj3mrQvksGHevPji8sRlI_L8

# Deploy
railway up
```

---

## 3. Test Your Bot

1. Open Telegram

2. Search for your bot username (the one you gave @BotFather)

3. Send `/start`

4. You should receive the welcome message!

5. Complete onboarding: `/onboarding`

6. Try your first daily check-in: `/daily`

---

## Expected Bot Behavior

### On First `/start`:
```
👋 Welcome to your CEO Personal Operating System.

This is a private, single-user productivity system designed for founders,
CEOs, and operators who want clarity without complexity.

I'll help you with:
• Daily check-ins (5 min)
• Weekly reviews (20 min)
• Quarterly evaluations (90 min)
• Annual reflection and planning
• Goal tracking and life design
• Pattern recognition

Let's start with a quick setup. This will take about 5 minutes.

Use /onboarding to begin, or /help to see all commands.
```

### Onboarding Flow (`/onboarding`):
- Asks for your name
- Asks for your role (CEO, Founder, etc.)
- Asks for company name
- Asks for stage of life
- Asks for timezone
- Asks for daily reminder time
- Confirms setup complete

### Daily Check-in (`/daily`):
- Energy level (1-10)
- One meaningful win
- One friction point
- One thing to let go of
- One priority for tomorrow
- Optional notes

### Weekly Review (`/weekly`):
- What moved the needle
- What was noise
- Where time leaked
- Energy reflection
- Strategic insight
- Adjustment for next week

---

## Troubleshooting

### Bot doesn't respond:
1. Check Railway logs for errors
2. Verify `TELEGRAM_BOT_TOKEN` is set correctly
3. Verify root directory is set to `ceo-personal-os-bot`
4. Check that the deployment succeeded

### "Module not found" errors in logs:
- Railway should auto-install from `requirements.txt`
- If not, add build command in Settings:
  - Build Command: `pip install -r requirements.txt`

### Bot starts but crashes:
- Check logs for Python errors
- Verify all files are present in the deployment

### Reminders not working:
- Make sure the bot process stays running (Railway handles this)
- Check that you completed `/onboarding` with your timezone

---

## Monitoring

**View Logs:**
- Go to your Railway project
- Click on your service
- Click **"Logs"** tab
- You'll see real-time output from the bot

**Check Status:**
- In Railway, your service should show **"Active"** with a green dot

**Database:**
- SQLite database is created automatically at `ceo_personal_os.db`
- Stored in Railway's ephemeral filesystem
- **Important:** If you redeploy, the database is reset (data is lost)
- For persistent data, upgrade to Railway's volume storage or use PostgreSQL

---

## Upgrading to Persistent Database (Optional)

To keep your data across redeploys:

**Option 1: Railway Volume (Recommended)**
1. In Railway, go to your service
2. Click **"Settings"**
3. Under **"Volumes"**, click **"Add Volume"**
4. Mount path: `/data`
5. Update `.env` variable:
   - `DATABASE_URL=sqlite:////data/ceo_personal_os.db`

**Option 2: PostgreSQL**
1. In Railway, click **"New"** → **"Database"** → **"PostgreSQL"**
2. Railway auto-creates `DATABASE_URL` variable
3. Bot automatically uses PostgreSQL instead of SQLite

---

## Cost

**Railway Pricing:**
- Free tier: $5 credit per month
- Your bot uses ~$0.50-1.00/month
- **You have plenty of free credits**

**Scaling:**
- Bot handles 1 user (you) perfectly
- No scaling needed

---

## Next Steps After Deployment

1. ✅ Deploy to Railway (following steps above)
2. ✅ Open Telegram and message your bot
3. ✅ Send `/start`
4. ✅ Complete `/onboarding`
5. ✅ Do your first `/daily` check-in
6. ✅ Set your first goal with `/setgoal`
7. ✅ Complete the Identity & Values interview (`/interviews`)

---

## Need Help?

**Check:**
1. Railway logs (most issues show up there)
2. `ceo-personal-os-bot/README.md` (full documentation)
3. Bot `/help` command (once it's running)

**Common Issues:**
- Bot token incorrect → Double-check the token
- Root directory not set → Must be `ceo-personal-os-bot`
- Build fails → Check Railway build logs

---

## Your Bot Details

- **Token:** `8590281913:AAG6VwGKy6iGj3mrQvksGHevPji8sRlI_L8`
- **Repository:** `mferdickbutt/CEO`
- **Branch:** `claude/ceo-personal-os-GoqXy`
- **Directory:** `ceo-personal-os-bot`
- **Default Timezone:** UTC (you can update in `/onboarding`)

---

🎯 **You're all set! Deploy to Railway and start using your personal operating system.**
