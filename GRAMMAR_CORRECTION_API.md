# 🧠 Grammarly++ Grammar Correction API

## ✅ Implementation Complete

The Grammarly++ style grammar correction engine has been fully integrated into EduLingua Pro!

## 🚀 New Endpoint

### POST `/grammar/correct`

**Comprehensive grammar correction with explanations and rephrasing.**

#### Request Body:
```json
{
  "text": "name Nishanth I",
  "style": "fluent",  // optional: "formal", "concise", "fluent", "casual"
  "num_variants": 3   // optional: number of rephrased variants (1-5)
}
```

#### Response:
```json
{
  "original": "name Nishanth I",
  "corrected": "My name is Nishanth.",
  "rephrased_variants": [
    {
      "text": "I am Nishanth.",
      "style": "concise",
      "rank": 1
    },
    {
      "text": "My name's Nishanth.",
      "style": "casual",
      "rank": 2
    }
  ],
  "explanations": {
    "summary": "Restructured sentence to follow English word order | Added missing articles.",
    "explanations": [
      {
        "type": "word_order",
        "message": "Sentence structure corrected: English follows Subject-Verb-Object order.",
        "rule": "English sentence structure: 'My name is [name]' is the standard format.",
        "example": "❌ 'name Nishanth I' → ✅ 'My name is Nishanth.'"
      }
    ],
    "errors": [],
    "suggestions": ["My name is Nishanth"],
    "correction_applied": true
  },
  "adaptive_feedback": {
    "feedback": "Work on sentence structure and word order.",
    "recommendations": [
      {
        "topic": "English Word Order",
        "description": "Learn Subject-Verb-Object (SVO) structure",
        "practice": "Practice: 'My name is [name]', 'I like to [verb]'"
      }
    ],
    "focus_areas": ["Sentence Structure"],
    "learning_tips": [
      "English follows Subject-Verb-Object order. Example: 'I eat apples' not 'Eat I apples'."
    ],
    "error_summary": {
      "total_errors": 2,
      "unique_error_types": 2,
      "most_common": "word_order",
      "progress_score": 80
    }
  },
  "correction_method": "rule_based",
  "error_count": 2
}
```

## 📋 Additional Endpoints

### GET `/grammar/lesson/{error_type}`

Get personalized lesson for a specific error type.

**Example:**
```bash
GET /grammar/lesson/missing_article
```

**Response:**
```json
{
  "title": "Using Articles: A, An, The",
  "level": "A1-A2",
  "content": "Articles are words that come before nouns...",
  "examples": [
    "I am a student. (consonant sound)",
    "I am an engineer. (vowel sound)"
  ],
  "practice": "Try: 'I am ___ student' → 'I am a student'"
}
```

### GET `/grammar/history`

Get user's grammar correction history (requires authentication).

**Response:**
```json
{
  "history": [
    {
      "original": "i nishanth name",
      "corrected": "My name is Nishanth.",
      "error_types": ["word_order", "missing_words"],
      "error_count": 2,
      "timestamp": "2025-11-13T12:00:00Z"
    }
  ],
  "total": 10
}
```

## 🧩 Features

### ✅ Grammar Correction
- **T5 Model**: Uses `vennify/t5-base-grammar-correction` for advanced corrections
- **Rule-based Fallback**: Falls back to rule-based correction if model unavailable
- **Multiple Methods**: Tracks correction method used

### ✅ Rephrasing Variants
- **Pegasus Model**: Uses `tuner007/pegasus_paraphrase` for natural rephrasing
- **Style Options**: Formal, concise, fluent, casual
- **Multiple Variants**: Generates 1-5 rephrased versions

### ✅ Detailed Explanations
- **LanguageTool**: Uses LanguageTool for error detection
- **Rule-based**: Provides grammar rule explanations
- **Context-aware**: Explains why corrections were made

### ✅ Adaptive Feedback
- **Personalized**: Based on user's error patterns
- **Learning Tips**: Provides actionable learning advice
- **Progress Tracking**: Calculates progress scores
- **Recommendations**: Suggests specific topics to focus on

### ✅ History & Analytics
- **Logging**: Stores all corrections in MongoDB
- **Error Tracking**: Tracks error types and frequencies
- **User Analytics**: Provides insights into learning patterns

## 🧪 Test the API

```bash
# Test grammar correction
curl -X POST http://localhost:8000/grammar/correct \
  -H "Content-Type: application/json" \
  -d '{"text": "name Nishanth I", "num_variants": 3}'

# Test with authentication
curl -X POST http://localhost:8000/grammar/correct \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"text": "i like play football", "style": "fluent"}'
```

## 🔧 Integration with Frontend

The endpoint is ready to be integrated with your React frontend. You can:

1. **Add to API service** (`frontend/src/services/api.js`):
```javascript
export const correctGrammar = async (text, style = null, numVariants = 3) => {
  const response = await api.post('/grammar/correct', {
    text,
    style,
    num_variants: numVariants
  });
  return response.data;
};
```

2. **Use in Dashboard component** to show:
   - Corrected sentence
   - Multiple rephrased variants
   - Detailed explanations
   - Adaptive learning feedback

## 📊 Database Schema

Grammar corrections are stored in `grammar_logs` collection:

```javascript
{
  user_id: ObjectId,
  original_text: String,
  corrected_text: String,
  error_types: [String],
  error_count: Number,
  correction_method: String,
  explanations: [Object],
  timestamp: DateTime
}
```

## 🎯 Next Steps

1. **Frontend Integration**: Connect the API to React components
2. **UI Enhancement**: Display corrections, variants, and explanations beautifully
3. **Real-time Correction**: Add live correction as user types
4. **Advanced Features**: Tone control, style preferences, etc.

---

**The Grammarly++ engine is fully operational! 🚀**

