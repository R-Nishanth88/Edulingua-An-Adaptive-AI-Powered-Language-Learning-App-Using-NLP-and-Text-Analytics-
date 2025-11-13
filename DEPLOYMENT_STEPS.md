# 🚀 Step-by-Step Deployment Instructions

## Prerequisites Checklist
- [ ] GitHub repository with your code
- [ ] MongoDB Atlas account (or use Render's MongoDB)
- [ ] OpenAI API key (for AI features)
- [ ] Render account (free tier available)
- [ ] Vercel account (free tier available)

---

## 📦 Step 1: Prepare Your Code

### 1.1 Commit and Push to GitHub
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 1.2 Verify Files
Make sure these files exist:
- ✅ `backend/requirements.txt`
- ✅ `backend/app.py`
- ✅ `frontend/package.json`
- ✅ `frontend/vite.config.js`

---

## 🔧 Step 2: Deploy Backend to Render

### 2.1 Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

### 2.2 Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select your repository

### 2.3 Configure Service
**Basic Settings:**
- **Name**: `edulingua-backend`
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: `backend` (if backend is in subdirectory)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### 2.4 Set Environment Variables
Click **"Environment"** tab and add:

```
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=edulingua
SECRET_KEY=<generate-random-32-char-string>
CORS_ORIGINS=https://your-app.vercel.app,https://*.vercel.app
OPENAI_API_KEY=sk-or-v1-your-key-here
OPENAI_API_BASE=https://openrouter.ai/api/v1
OPENAI_MODEL=openai/gpt-3.5-turbo
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2.5 Deploy
1. Click **"Create Web Service"**
2. Wait for build to complete (~5-10 minutes)
3. Copy your backend URL: `https://edulingua-backend.onrender.com`

**⚠️ Note**: Free tier services spin down after 15 min inactivity. First request takes ~30s.

---

## 🎨 Step 3: Deploy Frontend to Vercel

### 3.1 Install Vercel CLI
```bash
npm install -g vercel
```

### 3.2 Login to Vercel
```bash
vercel login
```

### 3.3 Navigate to Frontend
```bash
cd frontend
```

### 3.4 Deploy
```bash
vercel
```

**Follow prompts:**
- Set up and deploy? → **Yes**
- Which scope? → **Your account**
- Link to existing project? → **No**
- Project name? → **edulingua-frontend** (or your choice)
- Directory? → **./**
- Override settings? → **No**

### 3.5 Add Environment Variable
```bash
vercel env add VITE_API_URL production
```
Enter: `https://edulingua-backend.onrender.com`

### 3.6 Production Deploy
```bash
vercel --prod
```

### 3.7 Get Your Frontend URL
After deployment, Vercel will show your URL:
`https://edulingua-frontend.vercel.app`

---

## 🔄 Step 4: Update CORS

### 4.1 Update Render Environment Variable
1. Go to Render Dashboard
2. Select your backend service
3. Go to **Environment** tab
4. Update `CORS_ORIGINS`:
   ```
   https://your-frontend-url.vercel.app,https://*.vercel.app
   ```
5. Click **"Save Changes"**
6. Service will auto-restart

---

## 🗄️ Step 5: MongoDB Atlas Setup (If needed)

### 5.1 Create Cluster
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free cluster (M0)
3. Choose region closest to Render

### 5.2 Create Database User
1. Go to **Database Access**
2. Click **"Add New Database User"**
3. Username/Password authentication
4. Save credentials securely

### 5.3 Network Access
1. Go to **Network Access**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (0.0.0.0/0)
   - Or add Render's IP ranges

### 5.4 Get Connection String
1. Go to **Clusters** → **Connect**
2. Choose **"Connect your application"**
3. Copy connection string:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/
   ```
4. Update `DATABASE_URL` in Render

---

## ✅ Step 6: Verify Deployment

### 6.1 Test Backend
```bash
curl https://edulingua-backend.onrender.com/health
```
Should return: `{"status":"healthy"}`

### 6.2 Test Frontend
1. Visit your Vercel URL
2. Try to sign up
3. Check browser console for errors
4. Test login functionality

### 6.3 Check Logs
**Render**: Dashboard → Service → Logs
**Vercel**: Dashboard → Project → Functions → Logs

---

## 🔧 Troubleshooting

### Backend Issues

**500 Error:**
- Check Render logs
- Verify all environment variables
- Check database connection

**CORS Error:**
- Update CORS_ORIGINS with exact Vercel URL
- Restart Render service

**Slow Response:**
- Normal on free tier (cold start)
- First request: ~30 seconds
- Subsequent: ~2-5 seconds

### Frontend Issues

**API Calls Fail:**
- Check `VITE_API_URL` in Vercel
- Verify backend URL is correct
- Check CORS configuration

**Build Fails:**
- Check Node.js version (18+)
- Verify all dependencies
- Check Vercel build logs

---

## 📊 Monitoring

### Render
- **Logs**: Real-time in dashboard
- **Metrics**: CPU, Memory, Response time
- **Events**: Deployments, restarts

### Vercel
- **Analytics**: Page views, performance
- **Logs**: Function logs, errors
- **Deployments**: Build history

---

## 🔐 Security Checklist

- [ ] SECRET_KEY is strong and random
- [ ] CORS_ORIGINS restricted to your domain
- [ ] MongoDB IP whitelist configured
- [ ] API keys not in code (use env vars)
- [ ] HTTPS enabled (automatic on both platforms)

---

## 🎉 Success!

Your app is now live:
- **Frontend**: https://your-app.vercel.app
- **Backend**: https://edulingua-backend.onrender.com

Share your app URL and start using EduLingua Pro! 🚀

