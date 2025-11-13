# 🚀 Starting EduLingua Pro Application

## ✅ Application Status

Both servers are starting in the background!

## 🌐 Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 Quick Commands

### Start Backend
```bash
cd backend
source venv/bin/activate
uvicorn app:app --reload --port 8000
```

### Start Frontend
```bash
cd frontend
npm run dev
```

### Stop Servers
```bash
# Kill backend (port 8000)
lsof -ti:8000 | xargs kill

# Kill frontend (port 5173)
lsof -ti:5173 | xargs kill

# Kill both
lsof -ti:8000,5173 | xargs kill
```

## 🔍 Verify Servers

```bash
# Check backend
curl http://localhost:8000/health

# Check frontend
curl http://localhost:5173/
```

## 📝 MongoDB Setup

Before using the app, ensure MongoDB is running:

```bash
# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod

# Or use MongoDB Atlas (cloud)
```

Update `backend/.env`:
```env
DATABASE_URL=mongodb://localhost:27017
DATABASE_NAME=edulingua
```

## 🎯 First Steps

1. Open http://localhost:5173 in your browser
2. Sign up for a new account
3. Start analyzing your English text!

---

**The application is now running! 🎉**
