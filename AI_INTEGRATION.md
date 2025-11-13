# 🤖 AI Integration Guide

## Overview
EduLingua Pro now integrates with OpenAI-compatible APIs (OpenRouter) to provide enhanced, intelligent responses throughout the application.

## API Configuration

The AI service is configured to use:
- **API Provider**: OpenRouter (OpenAI-compatible)
- **API Key**: Configured in `backend/core/ai_service.py`
- **Default Model**: `openai/gpt-3.5-turbo`
- **Base URL**: `https://openrouter.ai/api/v1`

## Features Enhanced with AI

### 1. **Chatbot** 🤖
- **Enhanced Responses**: More natural, context-aware conversations
- **Better Explanations**: Detailed grammar and vocabulary explanations
- **Contextual Understanding**: Remembers previous conversation turns

### 2. **Dialog Practice** 💬
- **Natural Conversations**: More realistic dialog responses
- **Topic-Aware**: Responses adapt to conversation topic
- **Engaging Interactions**: More varied and interesting replies

### 3. **Grammar Explanations** 📚
- **Detailed Explanations**: AI-generated explanations for grammar corrections
- **Educational Content**: Clear, helpful explanations with examples
- **Error-Specific**: Tailored explanations for different error types

### 4. **Text Rephrasing** ✍️
- **Style-Aware**: Rephrases text in different styles (formal, concise, fluent)
- **Quality Improvements**: Better rephrasing quality than rule-based methods
- **Context Preservation**: Maintains original meaning while improving style

### 5. **Difficulty Adjustment** 📊
- **Smart Rephrasing**: Automatically adjusts text difficulty using AI
- **Level-Appropriate**: Generates text suitable for user's proficiency level
- **Natural Language**: More natural than rule-based simplification

## Configuration

### Environment Variables (Optional)
You can override the default configuration using environment variables:

```bash
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_API_BASE="https://openrouter.ai/api/v1"
export OPENAI_MODEL="openai/gpt-3.5-turbo"
```

### Model Options
You can use different models by changing `OPENAI_MODEL`:
- `openai/gpt-3.5-turbo` (default, fast and cost-effective)
- `openai/gpt-4` (more capable, slower)
- `anthropic/claude-3-haiku` (alternative provider)
- `google/gemini-pro` (alternative provider)

## Fallback Behavior

The application gracefully falls back to rule-based responses if:
- AI service is unavailable
- API key is invalid
- Network errors occur
- Rate limits are exceeded

This ensures the application always works, even without AI.

## Usage Examples

### Chatbot
```python
# Automatically uses AI if available
response = generate_intelligent_response("Explain articles in grammar")
```

### Dialog Practice
```python
# AI-enhanced dialog responses
response = generate_response("who are you", context, "introductions")
```

### Grammar Explanation
```python
# Detailed AI explanations
explanation = explain_correction(
    "i am student",
    "I am a student",
    "article",
    detailed=True
)
```

### Rephrasing
```python
# AI-powered rephrasing
variants = rephrase_text("My name is John", style="formal")
```

## Cost Considerations

- **GPT-3.5-turbo**: ~$0.002 per 1K tokens (very affordable)
- **GPT-4**: ~$0.03 per 1K tokens (more expensive)
- Responses are typically 50-200 tokens

## Security

- API key is stored in code (for development)
- For production, use environment variables
- Never commit API keys to version control
- Consider using a secrets management service

## Testing

Test the AI integration:
```bash
# Test chatbot
curl -X POST http://localhost:8000/chatbot/ask \
  -H "Content-Type: application/json" \
  -d '{"query":"who are you"}'

# Test dialog
curl -X POST http://localhost:8000/advanced/dialog/respond \
  -H "Content-Type: application/json" \
  -d '{"user_input":"hello","context":[],"topic":"introductions"}'
```

## Troubleshooting

### AI Not Working
1. Check API key is correct
2. Verify network connectivity
3. Check API service status
4. Review backend logs for errors

### Fallback to Rule-Based
- This is normal if AI is unavailable
- Application will still function
- Check logs for specific error messages

## Future Enhancements

Potential improvements:
- [ ] Caching AI responses for common queries
- [ ] Fine-tuning models for education-specific tasks
- [ ] Multi-language support
- [ ] Voice interaction
- [ ] Personalized learning paths with AI

---

**Note**: The AI integration enhances but doesn't replace rule-based systems. Both work together to provide the best experience.

