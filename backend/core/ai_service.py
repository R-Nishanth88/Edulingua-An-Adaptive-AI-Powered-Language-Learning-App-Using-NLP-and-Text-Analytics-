"""
AI Service Module - Integrates OpenAI-compatible API for enhanced responses.
Uses OpenRouter or OpenAI-compatible API for intelligent text generation.
"""
from typing import List, Dict, Optional
import os
import json

# Try to import OpenAI library
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None

# API Configuration
API_KEY = os.getenv("OPENAI_API_KEY", "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")
API_BASE = os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")  # OpenRouter endpoint
MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-3.5-turbo")  # Default model

# Initialize OpenAI client if available (lazy initialization)
client = None

def get_client():
    """Get or initialize OpenAI client."""
    global client
    if client is not None:
        return client
    
    if not OPENAI_AVAILABLE or not API_KEY:
        return None
    
    try:
        # For OpenRouter, we need to set the HTTP headers
        client = openai.OpenAI(
            api_key=API_KEY,
            base_url=API_BASE,
            default_headers={
                "HTTP-Referer": "https://edulingua-pro.app",  # Optional: for OpenRouter analytics
                "X-Title": "EduLingua Pro"  # Optional: for OpenRouter analytics
            }
        )
        print("✅ AI Service initialized with OpenAI-compatible API")
        return client
    except Exception as e:
        print(f"⚠️ Could not initialize AI client: {e}")
        print(f"   API Key: {API_KEY[:10]}...")
        print(f"   Base URL: {API_BASE}")
        return None

def generate_ai_response(prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 200, temperature: float = 0.7) -> Optional[str]:
    """
    Generate AI response using OpenAI-compatible API.
    
    Args:
        prompt: User's prompt/question
        system_prompt: System instruction for the AI
        max_tokens: Maximum tokens in response
        temperature: Creativity level (0-1)
    
    Returns:
        Generated response text or None if unavailable
    """
    ai_client = get_client()
    if not ai_client or not API_KEY:
        return None
    
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = ai_client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        if response and response.choices:
            return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ Error generating AI response: {e}")
        return None
    
    return None

def enhance_chatbot_response(user_query: str, context: Optional[List[Dict]] = None) -> Optional[str]:
    """
    Enhance chatbot response using AI.
    Focused on grammar and EduLingua features.
    
    Args:
        user_query: User's question
        context: Previous conversation context
    
    Returns:
        Enhanced AI response or None
    """
    system_prompt = """You are EduLingua Pro, an AI English grammar tutor and language learning assistant. Your primary focus is:

**Grammar & Language Learning:**
- Grammar correction and detailed explanations
- Sentence structure and word order
- Parts of speech (articles, prepositions, tenses, etc.)
- Common grammar mistakes and how to fix them
- English language rules and patterns

**EduLingua Features:**
- Text analysis and grammar checking
- Vocabulary building and word usage
- Writing improvement and style feedback
- Progress tracking and personalized learning

**Your Role:**
- Be educational, clear, and encouraging
- Focus ONLY on grammar, vocabulary, and English learning
- Provide specific examples and explanations
- Help users understand WHY corrections are made
- Guide users to use EduLingua's features (dashboard analysis, grammar checker, etc.)

**Important:**
- Stay focused on English learning topics
- If asked about non-grammar topics, politely redirect to grammar/English learning
- Always provide actionable advice and examples
- Encourage users to use the dashboard for text analysis"""
    
    # Build context if available
    prompt = user_query
    if context and len(context) > 0:
        context_text = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in context[-3:]])
        prompt = f"Previous conversation:\n{context_text}\n\nUser: {user_query}\n\nYou:"
    
    return generate_ai_response(prompt, system_prompt, max_tokens=300, temperature=0.7)

def enhance_dialog_response(user_input: str, topic: str, context: Optional[List[Dict]] = None) -> Optional[str]:
    """
    Enhance dialog practice response using AI.
    
    Args:
        user_input: User's message in dialog
        topic: Conversation topic
        context: Previous dialog exchanges
    
    Returns:
        Enhanced AI response or None
    """
    system_prompt = f"""You are Alex, an English conversation partner. You're practicing a conversation about {topic}.
- Be natural and conversational
- Ask follow-up questions
- Keep responses appropriate for the topic
- Be friendly and encouraging"""
    
    # Build context
    prompt = user_input
    if context and len(context) > 0:
        context_text = "\n".join([f"{ex.get('speaker', 'Person')}: {ex.get('text', '')}" for ex in context[-3:]])
        prompt = f"Conversation so far:\n{context_text}\n\nUser: {user_input}\n\nYou (Alex):"
    
    return generate_ai_response(prompt, system_prompt, max_tokens=150, temperature=0.8)

def generate_grammar_explanation(error_type: str, original: str, corrected: str) -> Optional[str]:
    """
    Generate detailed grammar explanation using AI.
    
    Args:
        error_type: Type of grammar error
        original: Original incorrect text
        corrected: Corrected text
    
    Returns:
        Detailed explanation or None
    """
    system_prompt = """You are an English grammar expert. Explain grammar corrections clearly and helpfully."""
    
    prompt = f"""Explain this grammar correction:

Error Type: {error_type}
Original: {original}
Corrected: {corrected}

Provide a clear, educational explanation (2-3 sentences) about why this correction was made."""
    
    return generate_ai_response(prompt, system_prompt, max_tokens=150, temperature=0.5)

def generate_writing_feedback(text: str, focus_areas: Optional[List[str]] = None) -> Optional[str]:
    """
    Generate writing feedback using AI.
    
    Args:
        text: User's written text
        focus_areas: Areas to focus on (e.g., ["clarity", "conciseness"])
    
    Returns:
        Writing feedback or None
    """
    system_prompt = """You are a writing tutor. Provide constructive, encouraging feedback on writing."""
    
    focus = ", ".join(focus_areas) if focus_areas else "overall quality"
    prompt = f"""Provide feedback on this text, focusing on {focus}:

{text}

Give 2-3 specific suggestions for improvement."""
    
    return generate_ai_response(prompt, system_prompt, max_tokens=200, temperature=0.6)

def rephrase_with_ai(text: str, style: str = "fluent") -> Optional[str]:
    """
    Rephrase text using AI.
    
    Args:
        text: Text to rephrase
        style: Desired style ("formal", "concise", "fluent", "casual")
    
    Returns:
        Rephrased text or None
    """
    system_prompt = f"""You are a text rephrasing expert. Rephrase text in a {style} style while maintaining the original meaning."""
    
    prompt = f"Rephrase this text in a {style} style:\n\n{text}"
    
    return generate_ai_response(prompt, system_prompt, max_tokens=200, temperature=0.7)

def is_ai_available() -> bool:
    """Check if AI service is available."""
    if not OPENAI_AVAILABLE or not API_KEY:
        return False
    # Try to get client (will initialize if needed)
    try:
        return get_client() is not None
    except:
        return False

