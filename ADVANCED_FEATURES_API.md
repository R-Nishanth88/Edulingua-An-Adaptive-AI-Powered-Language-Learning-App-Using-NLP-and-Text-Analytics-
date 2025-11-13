# 🚀 Advanced Features API Documentation

## ✅ All Features Implemented

### 1. **Dialog Generation** 
**Endpoint:** `POST /advanced/dialog/generate`

Generate AI-powered conversational practice scenarios.

**Request:**
```json
{
  "topic": "introductions",
  "level": "B1",
  "num_exchanges": 5
}
```

**Response:**
```json
{
  "topic": "introductions",
  "level": "B1",
  "exchanges": [
    {"speaker": "Person A", "text": "Hello! My name is John.", "type": "greeting"},
    {"speaker": "Person B", "text": "Hi John! I'm Sarah. Nice to meet you.", "type": "greeting"}
  ],
  "scenario": "Professional networking event",
  "learning_objectives": ["Introduce yourself", "Ask about origin"],
  "vocabulary": ["introduce", "name", "from", "meet"]
}
```

---

### 2. **Error Pattern Mining**
**Endpoint:** `GET /advanced/error-patterns?days=30`

Tracks common mistakes per user and provides personalized improvement paths.

**Response:**
```json
{
  "total_errors": 45,
  "most_common_errors": {
    "missing_article": 15,
    "word_order": 12,
    "missing_infinitive": 8
  },
  "error_patterns": [
    {
      "pattern": "repeated_error",
      "error_type": "missing_article",
      "frequency": 15,
      "severity": "high"
    }
  ],
  "recommendations": [
    {
      "priority": "high",
      "error_type": "missing_article",
      "action": "Review article usage: 'a', 'an', 'the'",
      "practice_exercises": ["Fill in the blanks with articles"]
    }
  ]
}
```

---

### 3. **Adaptive Difficulty Modeling**
**Endpoint:** `GET /advanced/performance-level?days=30`

Adjusts complexity based on user performance.

**Response:**
```json
{
  "current_level": "B1",
  "performance_metrics": {
    "avg_error_rate": 0.3,
    "avg_readability": 65.5,
    "consistency": 0.75
  },
  "recommended_difficulty": {
    "min_sentence_length": 12,
    "max_sentence_length": 20,
    "min_flesch": 60,
    "vocabulary_complexity": "intermediate"
  }
}
```

**Endpoint:** `POST /advanced/difficulty/calculate`

Calculate text difficulty score.

**Endpoint:** `POST /advanced/difficulty/adjust`

Adjust text to target difficulty level.

---

### 4. **Keyword Extraction** ✅ (Already Exists)
**Endpoint:** `POST /advanced/keywords/extract`

Extract important terms for revision notes.

**Request:**
```json
{
  "text": "Your essay text here...",
  "top_n": 10
}
```

**Response:**
```json
{
  "keywords": [
    {"word": "important", "frequency": 5, "tf_score": 0.02, "importance": "high"},
    {"word": "concept", "frequency": 3, "tf_score": 0.01, "importance": "medium"}
  ],
  "count": 10
}
```

---

### 5. **Writing Style Feedback**
**Endpoint:** `POST /advanced/style/analyze`

Scores clarity, conciseness, coherence, formality, and structure.

**Request:**
```json
{
  "text": "Your text here..."
}
```

**Response:**
```json
{
  "overall_score": 75.5,
  "scores": {
    "clarity": 80.0,
    "conciseness": 70.0,
    "coherence": 75.0,
    "formality": 65.0,
    "structure": 85.0
  },
  "feedback": {
    "clarity": "Excellent clarity. Your writing is easy to understand.",
    "conciseness": "Generally concise. Look for opportunities to remove redundant words."
  },
  "strengths": ["Clarity", "Structure"],
  "improvements": ["Formality"],
  "recommendations": [
    "Use more formal vocabulary for professional contexts",
    "Vary sentence lengths for better rhythm"
  ]
}
```

---

### 6. **Semantic Similarity Scoring**
**Endpoint:** `POST /advanced/similarity/compare`

Compares learner-written sentences with target answers.

**Request:**
```json
{
  "learner_answer": "My name is Nishanth",
  "target_answer": "My name is Nishanth."
}
```

**Response:**
```json
{
  "similarity_score": 95.5,
  "grade": "A",
  "feedback": "Excellent! Your answer matches the target meaning very closely.",
  "key_differences": []
}
```

---

### 7. **Automatic Essay Scoring**
**Endpoint:** `POST /advanced/essay/score`

Grades essays using coherence, grammar, vocabulary, and argument strength.

**Request:**
```json
{
  "text": "Your essay text...",
  "topic": "Climate Change" // optional
}
```

**Response:**
```json
{
  "overall_score": 82.5,
  "grade": "B",
  "component_scores": {
    "grammar": 85.0,
    "vocabulary": 80.0,
    "coherence": 75.0,
    "structure": 90.0,
    "argument_strength": 70.0,
    "style": 85.0
  },
  "feedback": {
    "grammar": "Excellent grammar. Keep up the good work!",
    "vocabulary": "Good vocabulary. Minor improvements could be made."
  },
  "strengths": ["Grammar", "Structure"],
  "improvements": ["Argument"],
  "detailed_analysis": {
    "word_count": 250,
    "sentence_count": 12,
    "grammar_errors": 2,
    "readability": 65.5,
    "lexical_diversity": 0.72
  }
}
```

---

### 8. **Dialogue Act Classification**
**Endpoint:** `POST /advanced/dialogue/classify`

Detects user intent (question, request, greeting, etc.).

**Request:**
```json
{
  "text": "Can you help me with grammar?",
  "context": [] // optional
}
```

**Response:**
```json
{
  "act": "request",
  "confidence": 0.85,
  "alternatives": [
    {"act": "question", "confidence": 0.70}
  ],
  "suggested_response": "I'd be happy to help with that."
}
```

---

### 9. **Predictive Learning Path Generation**
**Endpoint:** `GET /advanced/learning-path?days=30`

Recommends next lessons using user performance analytics.

**Response:**
```json
{
  "current_level": "B1",
  "learning_path": {
    "next_lessons": [
      {
        "lesson_id": "lesson_1",
        "title": "Master Articles (a, an, the)",
        "topic": "Articles (a, an, the)",
        "priority": "high",
        "estimated_duration": "2-3 hours",
        "objectives": ["Learn when to use 'a', 'an', and 'the'"],
        "exercises": ["Fill in the blanks with articles"]
      }
    ],
    "priorities": [
      {
        "topic": "Articles (a, an, the)",
        "priority": "high",
        "reason": "Frequent missing_article errors (15 occurrences)"
      }
    ],
    "milestones": [
      {
        "milestone": "Reach B2 level",
        "progress": 65.5,
        "estimated_time": "2-3 months"
      }
    ]
  }
}
```

---

### 10. **Plagiarism & Repetition Detection**
**Endpoint:** `POST /advanced/plagiarism/check`

Ensures originality in written exercises.

**Request:**
```json
{
  "text": "Your text to check...",
  "reference_texts": ["Reference text 1", "Reference text 2"] // optional
}
```

**Response:**
```json
{
  "originality_score": 85.5,
  "repetition_score": 0.15,
  "plagiarism_risk": "low",
  "matches": [],
  "repetitive_phrases": [
    {"phrase": "for example", "count": 3}
  ],
  "recommendations": [
    "Reduce repetitive phrases. Use synonyms and varied expressions."
  ]
}
```

---

## 🎯 Integration Status

All features are:
- ✅ Implemented in backend modules
- ✅ Exposed via API endpoints
- ✅ Integrated into main app
- ✅ Ready for frontend integration

## 📡 Base URL

All endpoints are under `/advanced/` prefix:
- `http://localhost:8000/advanced/[endpoint]`

## 🔐 Authentication

Most endpoints support optional authentication:
- Use `get_current_user_optional` for public access
- Use `get_current_user` for user-specific features (error patterns, learning path)

---

**All advanced features are now live and ready to use! 🚀**

