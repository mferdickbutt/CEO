# 🔧 Railway Deployment Troubleshooting

## Your Deployment Failed - Here's How to Fix It

I've just pushed fixes for the most common Railway deployment issues. **Pull the latest changes first!**

---

## ✅ Step 1: Make Sure Railway Has Latest Code

Railway should automatically redeploy when you push, but if not:

1. Go to your Railway project
2. Click on your service
3. Click **"Deployments"** tab
4. Check if the latest commit is there: `Fix Railway deployment configuration`
5. If not, click **"Deploy"** → **"Redeploy"**

---

## 🔍 Common Railway Issues & Fixes

### Issue 1: "Error creating build plan with Railpack"

**Cause:** Railway can't detect the Python project properly.

**Fix:** I just added `nixpacks.toml` which explicitly tells Railway:
- Use Python 3.11
- Install from requirements.txt
- Run `python bot.py`

**What you need to do:**
1. Make sure the latest code is deployed (see Step 1)
2. Verify **Root Directory** is set to `ceo-personal-os-bot` (Settings tab)

---

### Issue 2: Build succeeds but bot doesn't start

**Check the logs for these errors:**

#### Error: "No module named 'telegram'"

**Fix:** Railway didn't install dependencies.

In Railway Settings, add:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python bot.py`

#### Error: "TELEGRAM_BOT_TOKEN not found"

**Fix:** Environment variable missing.

1. Go to **Variables** tab
2. Add:
   - Variable: `TELEGRAM_BOT_TOKEN`
   - Value: your bot token from @BotFather (no spaces or quotes)

#### Error: Database-related errors

**Fix:** SQLite permissions issue.

Add environment variable:
- Variable: `DATABASE_URL`
- Value: `sqlite:////tmp/ceo_personal_os.db`

---

### Issue 3: "Wrong root directory" or files not found

**Symptoms:** Build fails, can't find `bot.py`, can't find `requirements.txt`

**Fix:** Root directory not set correctly.

1. Click on your service
2. Go to **Settings** tab
3. Find **"Root Directory"** (under Service Settings section)
4. Enter exactly: `ceo-personal-os-bot`
5. Click the checkmark to save
6. Railway will redeploy automatically

---

### Issue 4: Bot starts but crashes immediately

**Check logs for:**
- Python syntax errors → File a GitHub issue
- Import errors → Dependencies not installed
- Connection errors → Bot token might be wrong

**Quick fix:**
1. Verify bot token is correct (no spaces, no quotes)
2. Check Python version in logs (should be 3.11)
3. Verify all dependencies installed

---

## 🚀 Alternative: Simplified Railway Setup

If you're still having issues, try this **from scratch**:

### Option A: Deploy Only the Bot Folder

1. **Create a NEW Railway project**
2. **Don't deploy from GitHub**
3. **Deploy using Railway CLI instead:**

```bash
# Install Railway CLI
npm i -g @railway/cli

# Navigate to bot folder
cd ceo-personal-os-bot

# Login to Railway
railway login

# Initialize new project
railway init

# Set environment variable
railway variables set TELEGRAM_BOT_TOKEN=<your_bot_token>

# Deploy
railway up
```

This uploads only the bot folder directly, avoiding any path issues.

---

### Option B: Use Render Instead

If Railway continues to fail, **Render.com** is another good option:

1. Go to **https://render.com**
2. Sign up with GitHub
3. Click **"New +"** → **"Background Worker"**
4. Connect repository: `mferdickbutt/CEO`
5. Branch: `claude/ceo-personal-os-GoqXy`
6. **Root Directory:** `ceo-personal-os-bot`
7. **Build Command:** `pip install -r requirements.txt`
8. **Start Command:** `python bot.py`
9. Add environment variable:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: your bot token from @BotFather
10. Click **"Create Background Worker"**

Render's free tier works great for this bot.

---

## 🐛 Debugging Checklist

Before asking for help, verify:

- [ ] Latest code is deployed (commit: `Fix Railway deployment configuration`)
- [ ] Root directory is set to `ceo-personal-os-bot`
- [ ] Environment variable `TELEGRAM_BOT_TOKEN` is set correctly
- [ ] Deployment status shows "Success" (green checkmark)
- [ ] Logs show `Starting CEO Personal OS Bot...`
- [ ] No error messages in logs

---

## 📋 What Should Successful Deployment Look Like?

### In Railway Dashboard:
- ✅ Service shows green dot (Active)
- ✅ Latest deployment shows "Success"

### In Logs (Deployments → View Logs):
```
Starting CEO Personal OS Bot...
INFO:apscheduler.scheduler:Scheduler started
INFO:telegram.ext.Application:Application started
```

### In Telegram:
- ✅ Bot responds to `/start`
- ✅ Bot shows welcome message

---

## 🆘 Still Not Working?

### Check These:

1. **Wrong branch?**
   - Make sure Railway is deploying `claude/ceo-personal-os-GoqXy`
   - Not `main` or `master`

2. **Old deployment cached?**
   - In Railway: Settings → Delete Service
   - Create new service
   - Redeploy fresh

3. **Bot token expired?**
   - Go to @BotFather in Telegram
   - Send `/mybots`
   - Select your bot
   - Check if token is still valid

4. **Railway free tier limit reached?**
   - Check your Railway usage dashboard
   - You should have $5/month in free credits

---

## 🎯 Nuclear Option: Start Fresh

If nothing works, here's the **guaranteed to work** method:

### Step 1: Create Standalone Bot Folder

```bash
# Go to your repo
cd /path/to/CEO

# Copy just the bot folder
cp -r ceo-personal-os-bot ~/standalone-bot

# Go to standalone folder
cd ~/standalone-bot

# Initialize new git repo
git init
git add .
git commit -m "CEO Personal OS Bot"

# Create new GitHub repo (via GitHub website)
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/ceo-bot.git
git push -u origin main
```

### Step 2: Deploy to Railway

1. Go to Railway
2. New Project → Deploy from GitHub
3. Select the NEW repo (ceo-bot)
4. No root directory needed (bot is at root)
5. Add `TELEGRAM_BOT_TOKEN` variable
6. Deploy!

This eliminates all path/structure issues.

---

## 📞 Getting Help

If you're still stuck after trying all this:

1. **Copy your Railway logs** (last 50 lines)
2. **Note which step failed** (build, deploy, runtime)
3. **Share any error messages**

I can help debug from there!

---

## ✅ Success Criteria

You'll know it's working when:

1. ✅ Railway deployment shows "Success"
2. ✅ Logs show "Application started"
3. ✅ Telegram bot responds to `/start`
4. ✅ You can complete `/onboarding`
5. ✅ You can do your first `/daily` check-in

**Once all 5 work, you're good to go!**

---

**Latest code pushed:** Railway deployment fixes
**Next step:** Redeploy on Railway and check logs
