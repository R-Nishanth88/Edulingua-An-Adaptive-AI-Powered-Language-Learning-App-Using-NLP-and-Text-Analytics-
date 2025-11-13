# 🚀 Quick Start Guide - EduLingua Pro

## ✅ Current Status

Both servers are **running**:
- **Backend**: http://localhost:8000 (API)
- **Frontend**: http://localhost:5173 (Web App)
- **API Docs**: http://localhost:8000/docs

---

## 📋 Setup Checklist

### ✅ Completed
- [x] Backend dependencies installed (core packages)
- [x] Frontend dependencies installed
- [x] NLTK data downloaded
- [x] Backend server started
- [x] Frontend server started
- [x] Environment files created

### ⚠️ Remaining Steps

1. **MySQL Database Setup** (Required)
   ```sql
   CREATE DATABASE edulingua;
   ```
   
   Then update `backend/.env`:
   ```env
   DATABASE_URL=mysql+pymysql://your_username:your_password@localhost:3306/edulingua
   ```

2. **spaCy Installation** (Optional - for advanced NLP)
   ```bash
   cd backend
   source venv/bin/activate
   pip install spacy
   python -m spacy download en_core_web_sm
   ```
   Note: spaCy has compatibility issues with Python 3.14. The app works without it!

---

## 🎯 How to Use

1. **Open the app**: http://localhost:5173
2. **Sign up** for a new account
3. **Start analyzing text** on the Dashboard
4. **Explore features**:
   - Grammar analysis
   - Vocabulary suggestions
   - Readability scoring
   - AI Chatbot
   - Progress tracking

---

## 🛑 Stopping the Servers

Press `Ctrl+C` in the terminal where the servers are running, or:

```bash
# Find and kill processes
lsof -ti:8000 | xargs kill  # Backend
lsof -ti:5173 | xargs kill  # Frontend
```

---

## 🔄 Restarting Servers

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn app:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

---

## 📝 Environment Variables

### Backend (`backend/.env`)
```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/edulingua
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:5173"]
```

### Frontend (`frontend/.env`)
```env
VITE_API_URL=http://localhost:8000
```

---

## 🐛 Troubleshooting

### Backend won't start
- Check MySQL is running: `mysql -u root -p`
- Verify database exists
- Check `backend/.env` credentials

### Frontend won't start
- Check port 5173 is free
- Verify `VITE_API_URL` in `frontend/.env`

### Database errors
- Ensure MySQL is installed and running
- Create database: `CREATE DATABASE edulingua;`
- Update credentials in `backend/.env`

---

## 🎓 Next Steps

1. Set up MySQL database
2. Update `.env` files
3. Restart servers
4. Start learning! 🚀

**Happy Learning with EduLingua Pro! 🧩**
