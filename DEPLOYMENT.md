# 🚀 Deployment Guide - EduLingua Pro

This guide will help you deploy EduLingua Pro to **Render** (Backend) and **Vercel** (Frontend).

## 📋 Prerequisites

1. **GitHub Account** - Your code should be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
4. **MongoDB Atlas Account** - For database (or use Render's MongoDB)

---

## 🔧 Part 1: Backend Deployment on Render

### Step 1: Prepare Backend for Production

1. **Update `backend/config.py`** to handle production environment variables:

```python
# Already configured to read from environment variables
```

2. **Create `backend/requirements.txt`** (if not exists):
```bash
cd backend
pip freeze > requirements.txt
```

### Step 2: Deploy to Render

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service**:
   - **Name**: `edulingua-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend` (if your backend is in a subdirectory)

5. **Add Environment Variables**:
   ```
   DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/
   DATABASE_NAME=edulingua
   SECRET_KEY=your-secret-key-here (generate a random string)
   CORS_ORIGINS=https://your-frontend.vercel.app,https://*.vercel.app
   OPENAI_API_KEY=your-openai-api-key
   OPENAI_API_BASE=https://openrouter.ai/api/v1
   OPENAI_MODEL=openai/gpt-3.5-turbo
   ```

6. **Click "Create Web Service"**

### Step 3: Get Backend URL

After deployment, Render will provide a URL like:
```
https://edulingua-backend.onrender.com
```

**Note**: Free tier services spin down after 15 minutes of inactivity. First request may take ~30 seconds.

---

## 🎨 Part 2: Frontend Deployment on Vercel

### Step 1: Prepare Frontend for Production

1. **Update API URL** in `frontend/src/services/api.js`:
```javascript
baseURL: import.meta.env.VITE_API_URL || "https://edulingua-backend.onrender.com"
```

2. **Create `.env.production`** in `frontend/`:
```
VITE_API_URL=https://edulingua-backend.onrender.com
```

### Step 2: Deploy to Vercel

#### Option A: Using Vercel CLI (Recommended)

1. **Install Vercel CLI**:
```bash
npm i -g vercel
```

2. **Login to Vercel**:
```bash
vercel login
```

3. **Navigate to frontend directory**:
```bash
cd frontend
```

4. **Deploy**:
```bash
vercel
```

5. **Follow the prompts**:
   - Set up and deploy? **Yes**
   - Which scope? **Your account**
   - Link to existing project? **No**
   - Project name? **edulingua-frontend**
   - Directory? **./**
   - Override settings? **No**

6. **Add Environment Variable**:
```bash
vercel env add VITE_API_URL
# Enter: https://edulingua-backend.onrender.com
```

7. **Redeploy with environment variable**:
```bash
vercel --prod
```

#### Option B: Using Vercel Dashboard

1. **Go to Vercel Dashboard**: https://vercel.com/dashboard
2. **Click "Add New..." → "Project"**
3. **Import your GitHub repository**
4. **Configure Project**:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

5. **Add Environment Variable**:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://edulingua-backend.onrender.com`

6. **Click "Deploy"**

### Step 3: Update CORS in Backend

After getting your Vercel URL, update the `CORS_ORIGINS` environment variable in Render:
```
CORS_ORIGINS=https://your-app.vercel.app,https://*.vercel.app
```

Then restart the Render service.

---

## 🗄️ Part 3: MongoDB Atlas Setup (If not using Render's MongoDB)

1. **Go to MongoDB Atlas**: https://www.mongodb.com/cloud/atlas
2. **Create a free cluster**
3. **Create a database user**
4. **Whitelist IP addresses** (or use `0.0.0.0/0` for all)
5. **Get connection string**:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/
   ```
6. **Update `DATABASE_URL` in Render**

---

## ✅ Post-Deployment Checklist

- [ ] Backend is accessible at Render URL
- [ ] Frontend is accessible at Vercel URL
- [ ] API calls from frontend work (check browser console)
- [ ] CORS is properly configured
- [ ] Environment variables are set correctly
- [ ] Database connection is working
- [ ] OpenAI API key is configured

---

## 🔍 Troubleshooting

### Backend Issues

**Problem**: Backend returns 500 errors
- Check Render logs
- Verify environment variables
- Check database connection

**Problem**: CORS errors
- Update `CORS_ORIGINS` with your Vercel URL
- Restart Render service

**Problem**: Slow first request
- Normal on free tier (cold start ~30s)
- Consider upgrading to paid tier

### Frontend Issues

**Problem**: API calls fail
- Check `VITE_API_URL` environment variable
- Verify backend URL is correct
- Check browser console for errors

**Problem**: Build fails
- Check Node.js version (should be 18+)
- Verify all dependencies in `package.json`
- Check build logs in Vercel

---

## 🔐 Security Best Practices

1. **Never commit** `.env` files
2. **Use strong SECRET_KEY** (generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
3. **Restrict CORS** to your domain only
4. **Use MongoDB Atlas IP whitelist**
5. **Rotate API keys** regularly

---

## 📊 Monitoring

### Render
- View logs: Dashboard → Your Service → Logs
- Monitor uptime: Dashboard → Your Service → Metrics

### Vercel
- View logs: Dashboard → Your Project → Functions → Logs
- Analytics: Dashboard → Your Project → Analytics

---

## 🚀 Quick Deploy Commands

### Backend (Render)
```bash
# Using Render CLI (if installed)
render services:create
```

### Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

---

## 📝 Environment Variables Reference

### Backend (Render)
```
DATABASE_URL=mongodb+srv://...
DATABASE_NAME=edulingua
SECRET_KEY=your-secret-key
CORS_ORIGINS=https://your-app.vercel.app
OPENAI_API_KEY=sk-...
OPENAI_API_BASE=https://openrouter.ai/api/v1
OPENAI_MODEL=openai/gpt-3.5-turbo
```

### Frontend (Vercel)
```
VITE_API_URL=https://edulingua-backend.onrender.com
```

---

## 🎉 Success!

Once deployed, your application will be live at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://edulingua-backend.onrender.com`

Test the deployment by visiting your frontend URL and trying to sign up/login!

