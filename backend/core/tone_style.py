from textblob import TextBlob
from typing import Dict, List
import re
from collections import Counter

def analyze_tone_and_style(text: str) -> Dict:
    """
    Analyze writing tone, style, and sentiment.
    """
    if not text or not text.strip():
        return {
            "sentiment": {"polarity": 0.0, "subjectivity": 0.0},
            "tone": "neutral",
            "style": "neutral",
            "formality": "neutral",
            "feedback": []
        }
    
    blob = TextBlob(text)
    
    # Sentiment analysis
    polarity = blob.sentiment.polarity  # -1 to 1
    subjectivity = blob.sentiment.subjectivity  # 0 to 1
    
    # Determine tone based on polarity
    if polarity > 0.3:
        tone = "positive"
    elif polarity < -0.3:
        tone = "negative"
    else:
        tone = "neutral"
    
    # Analyze formality
    formal_indicators = [
        r'\b(however|therefore|furthermore|moreover|consequently|nevertheless)\b',
        r'\b(utilize|facilitate|implement|demonstrate|analyze)\b',
        r'\b(according to|in accordance with|with regard to)\b'
    ]
    
    informal_indicators = [
        r'\b(yeah|yep|nope|gonna|wanna|gotta)\b',
        r'\b(cool|awesome|sucks|dude|hey)\b',
        r'(!{2,}|\?{2,})'  # Multiple exclamation/question marks
    ]
    
    formal_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in formal_indicators)
    informal_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in informal_indicators)
    
    if formal_count > informal_count * 2:
        formality = "formal"
    elif informal_count > formal_count * 2:
        formality = "informal"
    else:
        formality = "neutral"
    
    # Analyze style characteristics
    sentences = text.split('.')
    avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    
    # Check for verbosity
    word_count = len(text.split())
    unique_words = len(set(text.lower().split()))
    repetition_ratio = 1 - (unique_words / word_count) if word_count > 0 else 0
    
    style_feedback = []
    
    if avg_sentence_length > 25:
        style_feedback.append({
            "type": "sentence_length",
            "message": "Your sentences are quite long. Consider breaking them into shorter, clearer sentences.",
            "severity": "medium"
        })
    elif avg_sentence_length < 8:
        style_feedback.append({
            "type": "sentence_length",
            "message": "Your sentences are very short. Try combining some ideas for better flow.",
            "severity": "low"
        })
    
    if repetition_ratio > 0.3:
        style_feedback.append({
            "type": "repetition",
            "message": "You're repeating words frequently. Try using synonyms for variety.",
            "severity": "medium"
        })
    
    # Check for passive voice (simplified)
    passive_indicators = re.findall(r'\b(was|were|is|are|been)\s+\w+ed\b', text, re.IGNORECASE)
    if len(passive_indicators) > len(sentences) * 0.3:
        style_feedback.append({
            "type": "passive_voice",
            "message": "You're using passive voice frequently. Active voice is often clearer and more engaging.",
            "severity": "low"
        })
    
    # Determine overall style
    if formality == "formal" and avg_sentence_length > 20:
        style = "academic"
    elif formality == "informal" and avg_sentence_length < 15:
        style = "casual"
    else:
        style = "neutral"
    
    return {
        "sentiment": {
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3),
            "label": "positive" if polarity > 0.1 else "negative" if polarity < -0.1 else "neutral"
        },
        "tone": tone,
        "style": style,
        "formality": formality,
        "avg_sentence_length": round(avg_sentence_length, 2),
        "repetition_ratio": round(repetition_ratio, 3),
        "feedback": style_feedback
    }
