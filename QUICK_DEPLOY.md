# ⚡ Quick Deployment Guide

## 🚀 Deploy in 5 Minutes

### Backend (Render)

1. **Push code to GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Go to Render**: https://dashboard.render.com
3. **New → Web Service**
4. **Connect GitHub repo**
5. **Settings**:
   - Name: `edulingua-backend`
   - Build: `cd backend && pip install -r requirements.txt`
   - Start: `cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT`
6. **Environment Variables**:
   ```
   DATABASE_URL=your-mongodb-connection-string
   DATABASE_NAME=edulingua
   SECRET_KEY=generate-random-key
   CORS_ORIGINS=https://your-app.vercel.app
   OPENAI_API_KEY=your-key
   ```
7. **Deploy!**

### Frontend (Vercel)

1. **Install Vercel CLI**:
```bash
npm i -g vercel
```

2. **Deploy**:
```bash
cd frontend
vercel
```

3. **Add environment variable**:
```bash
vercel env add VITE_API_URL production
# Enter: https://edulingua-backend.onrender.com
```

4. **Redeploy**:
```bash
vercel --prod
```

**Done!** 🎉

