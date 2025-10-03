# VoteChain Morocco - Deployment Alternatives

## ⚠️ Why Not Vercel?

Vercel is **not suitable** for VoteChain Morocco because:
- ❌ No persistent file storage (blockchain.json would be lost on each deployment)
- ❌ Serverless functions have execution time limits
- ❌ Designed for frontend/Next.js apps, not Flask backends
- ❌ Cannot maintain stateful blockchain data

## ✅ Recommended Free Platforms

### 1. **Railway.app** (BEST OPTION - Recommended)

**Why Railway?**
- ✅ Free tier: $5 credit/month (enough for small projects)
- ✅ Persistent storage
- ✅ Easy GitHub integration
- ✅ Automatic deployments
- ✅ Custom domains
- ✅ Perfect for Flask apps

**How to Deploy:**

1. **Go to Railway.app**
   - Visit https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose: `imanologya1/Morocco-Referendum-`

3. **Configure Settings**
   - Railway auto-detects Python
   - Start command: `python src/main.py`
   - No additional config needed!

4. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Get your public URL!

**Configuration Files Included:**
- ✅ `railway.json` - Already in your repo
- ✅ `Procfile` - Already in your repo
- ✅ `requirements.txt` - Already in your repo

---

### 2. **Render.com** (ALSO GREAT)

**Why Render?**
- ✅ Free tier (750 hours/month)
- ✅ Persistent disks available
- ✅ GitHub auto-deploy
- ✅ Custom domains
- ✅ Easy to use

**How to Deploy:**

1. **Go to Render.com**
   - Visit https://render.com
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repo: `Morocco-Referendum-`

3. **Configure**
   - Name: `votechain-morocco`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python src/main.py`
   - Instance Type: `Free`

4. **Add Environment Variables**
   - `FLASK_ENV` = `production`
   - `PORT` = `10000` (Render's default)

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment
   - Get your URL!

**Configuration Files Included:**
- ✅ `render.yaml` - Already in your repo

---

### 3. **PythonAnywhere** (SIMPLE)

**Why PythonAnywhere?**
- ✅ Completely free tier
- ✅ No credit card required
- ✅ Persistent storage
- ✅ Python-focused

**How to Deploy:**

1. **Sign Up**
   - Visit https://www.pythonanywhere.com
   - Create free account

2. **Upload Code**
   - Go to "Files" tab
   - Upload your code or clone from GitHub:
   ```bash
   git clone https://github.com/imanologya1/Morocco-Referendum-.git
   ```

3. **Create Virtual Environment**
   ```bash
   cd Morocco-Referendum-
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Python 3.10
   - Set source code directory
   - Set WSGI file

5. **Reload and Visit**
   - Your app will be at: `yourusername.pythonanywhere.com`

---

### 4. **Fly.io** (ADVANCED)

**Why Fly.io?**
- ✅ Free tier
- ✅ Global deployment
- ✅ Persistent volumes
- ✅ Great performance

**How to Deploy:**

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   fly auth login
   ```

3. **Launch App**
   ```bash
   cd Morocco-Referendum-
   fly launch
   ```

4. **Follow Prompts**
   - App name: `votechain-morocco`
   - Region: Choose closest to Morocco (Europe)
   - Don't deploy PostgreSQL
   - Deploy now: Yes

5. **Access**
   - Your app: `votechain-morocco.fly.dev`

---

## 📋 Comparison Table

| Platform | Free Tier | Storage | Ease | Best For |
|----------|-----------|---------|------|----------|
| **Railway** | $5/month credit | ✅ Persistent | ⭐⭐⭐⭐⭐ | **Recommended** |
| **Render** | 750 hrs/month | ✅ Persistent | ⭐⭐⭐⭐⭐ | **Recommended** |
| **PythonAnywhere** | Always free | ✅ Persistent | ⭐⭐⭐⭐ | Beginners |
| **Fly.io** | Limited free | ✅ Volumes | ⭐⭐⭐ | Advanced |
| **Vercel** | ❌ Not suitable | ❌ No storage | ❌ | Frontend only |

---

## 🚀 Quick Start (Railway - Easiest)

1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `imanologya1/Morocco-Referendum-`
5. Wait 2 minutes
6. Done! 🎉

---

## 🔧 Troubleshooting

### "Module not found" Error
- Make sure `requirements.txt` is in the root directory
- Check build logs for missing dependencies

### "Port binding" Error
- The app now automatically uses the `PORT` environment variable
- Most platforms set this automatically

### "File not found" Error
- Check that `blockchain.json` and `polls.json` exist
- They should be created automatically on first run

### App Crashes on Startup
- Check logs in your platform's dashboard
- Verify Python version (3.11 recommended)
- Ensure all dependencies are installed

---

## 💡 Best Practice

**For Production:**
1. Use Railway or Render (most reliable)
2. Set up custom domain
3. Enable HTTPS (automatic on both platforms)
4. Set `FLASK_ENV=production`
5. Monitor logs regularly
6. Back up blockchain data weekly

---

## 🆘 Still Having Issues?

If you're still getting errors:

1. **Check the platform's logs** - They show exactly what's wrong
2. **Verify requirements.txt** - All dependencies must be listed
3. **Test locally first** - Make sure it runs on your computer
4. **Check Python version** - Should be 3.11

**Common Issues:**
- Missing `requirements.txt` → Already included ✅
- Wrong start command → Use `python src/main.py` ✅
- Port not configurable → Fixed in latest code ✅
- No persistent storage → Use Railway/Render ✅

---

## 📞 Need Help?

1. Check platform documentation
2. Review deployment logs
3. Test locally: `python src/main.py`
4. Verify all files are pushed to GitHub

**Your voting system is ready to deploy - just choose the right platform!** 🇲🇦
