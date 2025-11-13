"""
Emotion & Intent Analysis Module
Detects emotional tone (confident, polite, assertive, apologetic) and user intent.
"""
from typing import Dict, List, Optional
from core.ai_service import generate_ai_response, is_ai_available
from core.tone_style import analyze_tone_and_style

# Emotion categories
EMOTIONS = {
    "confident": {
        "keywords": ["certain", "sure", "definitely", "absolutely", "confident", "believe"],
        "description": "Expresses certainty and self-assurance"
    },
    "polite": {
        "keywords": ["please", "thank you", "appreciate", "kindly", "would you", "could you"],
        "description": "Shows respect and courtesy"
    },
    "assertive": {
        "keywords": ["must", "should", "need to", "require", "demand", "insist"],
        "description": "Expresses strong opinions or demands"
    },
    "apologetic": {
        "keywords": ["sorry", "apologize", "regret", "my fault", "excuse me", "pardon"],
        "description": "Expresses regret or apology"
    },
    "enthusiastic": {
        "keywords": ["excited", "thrilled", "amazing", "wonderful", "love", "great"],
        "description": "Shows excitement and positive energy"
    },
    "neutral": {
        "keywords": [],
        "description": "Neutral, factual tone"
    },
    "frustrated": {
        "keywords": ["frustrated", "annoyed", "upset", "disappointed", "unhappy"],
        "description": "Shows frustration or dissatisfaction"
    },
    "grateful": {
        "keywords": ["thankful", "grateful", "appreciate", "thanks", "blessed"],
        "description": "Expresses gratitude"
    }
}

# Intent categories
INTENTS = {
    "question": {
        "indicators": ["?", "what", "how", "why", "when", "where", "who", "which"],
        "description": "Asking for information"
    },
    "request": {
        "indicators": ["please", "could you", "would you", "can you", "help", "need"],
        "description": "Making a request"
    },
    "statement": {
        "indicators": ["i", "we", "they", "it is", "this is"],
        "description": "Stating information"
    },
    "command": {
        "indicators": ["do", "make", "go", "stop", "don't", "must", "should"],
        "description": "Giving a command or instruction"
    },
    "greeting": {
        "indicators": ["hello", "hi", "hey", "good morning", "good afternoon"],
        "description": "Greeting someone"
    },
    "correction": {
        "indicators": ["wrong", "error", "mistake", "correct", "fix", "should be"],
        "description": "Pointing out or requesting correction"
    }
}

def analyze_emotion(text: str, use_ai: bool = True) -> Dict:
    """
    Detect emotional tone in the text.
    
    Args:
        text: Input text to analyze
        use_ai: Whether to use AI for emotion detection
    
    Returns:
        Dictionary with detected emotion, confidence, and details
    """
    if not text or not text.strip():
        return {
            "detected_emotion": "neutral",
            "confidence": 0.0,
            "emotions": {}
        }
    
    text_lower = text.lower()
    
    # Use AI for emotion detection if available
    if use_ai and is_ai_available():
        try:
            prompt = f"""Analyze the emotional tone of this text. Choose the primary emotion from: confident, polite, assertive, apologetic, enthusiastic, neutral, frustrated, grateful.

Text: {text}

Respond with only the emotion name (e.g., "confident" or "polite")."""
            
            ai_emotion = generate_ai_response(
                prompt,
                "You are an emotion detection expert. Identify the primary emotional tone accurately.",
                max_tokens=20,
                temperature=0.3
            )
            
            if ai_emotion:
                detected = ai_emotion.strip().lower()
                if detected in EMOTIONS:
                    return {
                        "detected_emotion": detected,
                        "confidence": 0.85,
                        "emotion_info": EMOTIONS[detected],
                        "method": "ai_detection"
                    }
        except Exception as e:
            print(f"⚠️ AI emotion detection failed: {e}")
    
    # Fallback: rule-based detection
    emotion_scores = {}
    for emotion, info in EMOTIONS.items():
        if emotion == "neutral":
            continue
        score = sum(1 for keyword in info["keywords"] if keyword in text_lower)
        if score > 0:
            emotion_scores[emotion] = score
    
    if emotion_scores:
        # Get emotion with highest score
        detected_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = min(emotion_scores[detected_emotion] / 3.0, 1.0)  # Normalize
        
        return {
            "detected_emotion": detected_emotion,
            "confidence": confidence,
            "emotion_info": EMOTIONS[detected_emotion],
            "emotion_scores": emotion_scores,
            "method": "rule_based"
        }
    
    # Default to neutral
    return {
        "detected_emotion": "neutral",
        "confidence": 0.5,
        "emotion_info": EMOTIONS["neutral"],
        "method": "rule_based"
    }

def analyze_intent(text: str, use_ai: bool = True) -> Dict:
    """
    Detect user intent in the text.
    
    Args:
        text: Input text to analyze
        use_ai: Whether to use AI for intent detection
    
    Returns:
        Dictionary with detected intent, confidence, and details
    """
    if not text or not text.strip():
        return {
            "detected_intent": "statement",
            "confidence": 0.0
        }
    
    text_lower = text.lower()
    
    # Use AI for intent detection if available
    if use_ai and is_ai_available():
        try:
            prompt = f"""Analyze the intent of this text. Choose from: question, request, statement, command, greeting, correction.

Text: {text}

Respond with only the intent name (e.g., "question" or "request")."""
            
            ai_intent = generate_ai_response(
                prompt,
                "You are an intent classification expert. Identify the user's intent accurately.",
                max_tokens=20,
                temperature=0.3
            )
            
            if ai_intent:
                detected = ai_intent.strip().lower()
                if detected in INTENTS:
                    return {
                        "detected_intent": detected,
                        "confidence": 0.85,
                        "intent_info": INTENTS[detected],
                        "method": "ai_detection"
                    }
        except Exception as e:
            print(f"⚠️ AI intent detection failed: {e}")
    
    # Fallback: rule-based detection
    intent_scores = {}
    for intent, info in INTENTS.items():
        score = sum(1 for indicator in info["indicators"] if indicator in text_lower)
        if score > 0:
            intent_scores[intent] = score
    
    # Special handling for questions
    if "?" in text:
        intent_scores["question"] = intent_scores.get("question", 0) + 2
    
    if intent_scores:
        detected_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(intent_scores[detected_intent] / 2.0, 1.0)
        
        return {
            "detected_intent": detected_intent,
            "confidence": confidence,
            "intent_info": INTENTS[detected_intent],
            "intent_scores": intent_scores,
            "method": "rule_based"
        }
    
    # Default to statement
    return {
        "detected_intent": "statement",
        "confidence": 0.5,
        "intent_info": INTENTS["statement"],
        "method": "rule_based"
    }

def analyze_emotion_and_intent(text: str, use_ai: bool = True) -> Dict:
    """
    Combined analysis of emotion and intent.
    
    Returns:
        Dictionary with both emotion and intent analysis
    """
    emotion_result = analyze_emotion(text, use_ai=use_ai)
    intent_result = analyze_intent(text, use_ai=use_ai)
    
    return {
        "emotion": emotion_result,
        "intent": intent_result,
        "text": text,
        "summary": f"Emotion: {emotion_result['detected_emotion']}, Intent: {intent_result['detected_intent']}"
    }

