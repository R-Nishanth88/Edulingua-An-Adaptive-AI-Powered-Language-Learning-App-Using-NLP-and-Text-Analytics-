# 🧩 EduLingua Pro – Adaptive AI Language Learning Platform

A comprehensive full-stack AI-powered language learning system that helps users learn and improve their English writing skills using **text analytics, NLP, and adaptive learning**.

## 🎯 Features

- **Grammar Analysis**: Advanced NLP-powered grammar error detection and correction
- **Vocabulary Enhancement**: Lexical diversity analysis, synonym suggestions, and contextual recommendations
- **Readability Analysis**: Flesch Reading Ease, CEFR level prediction (A1-C2)
- **Tone & Style Analysis**: Sentiment analysis, formality detection, and style feedback
- **Proficiency Prediction**: ML-based CEFR level classification
- **AI Tutor Chatbot**: Interactive chatbot for grammar and vocabulary tutoring
- **Progress Tracking**: Visual dashboards with charts and analytics
- **Gamification**: XP points, badges, and achievements
- **Adaptive Recommendations**: Personalized learning content based on user level and errors

## 🏗️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **NLP Libraries**: spaCy, NLTK, TextBlob, textstat, Transformers (T5, BERT)
- **Database**: MongoDB with Beanie ODM
- **Authentication**: JWT-based
- **ML Models**: Sentence-BERT, T5, BART

### Frontend
- **Framework**: React 18 + Vite
- **Styling**: TailwindCSS
- **Charts**: Recharts
- **Routing**: React Router DOM
- **HTTP Client**: Axios

## 📁 Project Structure

```
EduLinguaPro/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── config.py             # Configuration settings
│   ├── requirements.txt       # Python dependencies
│   ├── routers/              # API route handlers
│   │   ├── analyze.py
│   │   ├── user.py
│   │   ├── chatbot.py
│   │   ├── gamify.py
│   │   ├── recommend.py
│   │   └── progress.py
│   ├── core/                 # NLP and business logic
│   │   ├── preprocessing.py
│   │   ├── grammar_analysis.py
│   │   ├── lexical_semantic.py
│   │   ├── readability.py
│   │   ├── tone_style.py
│   │   ├── proficiency_model.py
│   │   ├── summarizer_qg.py
│   │   ├── recommender.py
│   │   ├── error_mining.py
│   │   ├── explainable_ai.py
│   │   └── auth.py
│   └── models/               # Database models
│       ├── user_model.py
│       ├── progress_model.py
│       ├── feedback_model.py
│       ├── xp_model.py
│       ├── recommendation_model.py
│       └── database.py
│
├── frontend/
│   ├── src/
│   │   ├── pages/            # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── LoginSignup.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Chatbot.jsx
│   │   │   ├── Progress.jsx
│   │   │   └── VocabularyTrainer.jsx
│   │   ├── components/       # Reusable components
│   │   │   ├── TextAnalyzer.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   ├── GrammarHighlight.jsx
│   │   │   ├── Charts.jsx
│   │   │   ├── WordCloud.jsx
│   │   │   ├── Navbar.jsx
│   │   │   └── BadgeDisplay.jsx
│   │   ├── services/
│   │   │   └── api.js        # API service layer
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- MongoDB 6.0+ (or MongoDB Atlas)
- pip and npm

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Set up environment variables**:
   Create a `.env` file in the `backend` directory:
   ```env
   DATABASE_URL=mongodb://localhost:27017
   DATABASE_NAME=edulingua
   SECRET_KEY=your-secret-key-change-in-production
   CORS_ORIGINS=["http://localhost:5173"]
   ```

6. **Start MongoDB** (if running locally):
   ```bash
   # macOS (using Homebrew)
   brew services start mongodb-community
   
   # Linux
   sudo systemctl start mongod
   
   # Or use MongoDB Atlas (cloud) - just update DATABASE_URL in .env
   ```

7. **Database collections are created automatically** on first run - no migrations needed!

8. **Start the backend server**:
   ```bash
   uvicorn app:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Create environment file** (optional):
   Create a `.env` file in the `frontend` directory:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

4. **Start the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## 📊 API Endpoints

### Authentication
- `POST /user/signup` - User registration
- `POST /user/login` - User login (returns JWT token)
- `GET /user/me` - Get current user info

### Text Analysis
- `POST /analyze/` - Comprehensive text analysis
- `POST /analyze/summarize` - Summarize text
- `POST /analyze/questions` - Generate comprehension questions

### Chatbot
- `POST /chatbot/ask` - Chat with AI tutor

### Progress & Analytics
- `GET /progress/` - Get user progress data
- `GET /gamify/badges` - Get user badges
- `GET /gamify/leaderboard` - Get leaderboard
- `POST /gamify/xp` - Update XP points

### Recommendations
- `GET /recommend/` - Get adaptive learning recommendations

## 🧠 NLP Modules

### 1. Preprocessing
- Tokenization, lemmatization, POS tagging
- Named Entity Recognition (NER)
- Stopword removal

### 2. Grammar Analysis
- Rule-based error detection
- T5-based grammar correction
- Error highlighting and explanations

### 3. Vocabulary & Semantic Analysis
- Lexical diversity (TTR)
- Keyword extraction (TF-IDF)
- Synonym suggestions
- Semantic coherence analysis

### 4. Readability Analysis
- Flesch Reading Ease
- Gunning Fog Index
- CEFR level prediction (A1-C2)

### 5. Tone & Style Analysis
- Sentiment analysis (polarity, subjectivity)
- Formality detection
- Style feedback (verbosity, repetition)

### 6. Proficiency Classification
- Rule-based CEFR level prediction
- Confidence scoring
- Explainable predictions

## 🎮 Gamification

- **XP Points**: Earn points for completing analyses
- **Badges**: Unlock badges like "Grammar Guru", "Lexical Legend", "Fluency Pro"
- **Streaks**: Track consecutive practice days
- **Leaderboard**: Compare progress with other users

## 🗄️ Database Schema (MongoDB Collections)

### users
- _id (ObjectId), username, email, password (hashed), cefr_level, xp_points, created_at

### progress
- _id (ObjectId), user_id (ObjectId), date, grammar_errors, readability, sentiment, cefr_level, lexical_diversity

### feedback_logs
- _id (ObjectId), user_id (ObjectId), text, corrections (array), suggestions (array), created_at

### xp_badges
- _id (ObjectId), user_id (ObjectId), badge_name, earned_on

### recommendations
- _id (ObjectId), user_id (ObjectId), content_title, link, difficulty, content_type, created_at

## 🚢 Deployment

### Backend (Render)
1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in Render dashboard

### Frontend (Vercel)
1. Connect your GitHub repository
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Add environment variable: `VITE_API_URL` (your backend URL)

### Database (MongoDB Atlas)
1. Create a MongoDB Atlas cluster (free tier available)
2. Get your connection string
3. Update `DATABASE_URL` in backend environment variables:
   ```env
   DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/
   DATABASE_NAME=edulingua
   ```
4. Collections are created automatically on first run

## 🧪 Testing

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm test
```

## 📝 Notes

- The T5 and BART models are large and may take time to download on first run
- For production, consider using GPU acceleration for NLP models
- Some NLP models require significant memory; adjust batch sizes if needed
- The chatbot uses rule-based responses; can be enhanced with GPT/LLM integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- spaCy for NLP processing
- HuggingFace for transformer models
- FastAPI for the backend framework
- React and TailwindCSS for the frontend

---

**Built with ❤️ for language learners worldwide**
