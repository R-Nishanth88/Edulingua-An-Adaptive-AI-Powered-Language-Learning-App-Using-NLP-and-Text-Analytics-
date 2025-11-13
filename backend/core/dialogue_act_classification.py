"""
Dialogue Act Classification - Detects user intent in conversations.
Classifies dialogue acts: question, request, greeting, statement, etc.
"""
from typing import Dict, List, Optional
import re

def classify_dialogue_act(text: str, context: Optional[List[Dict]] = None) -> Dict:
    """
    Classify the dialogue act (intent) of user input.
    
    Args:
        text: User's input text
        context: Previous conversation context (optional)
    
    Returns:
        Dictionary with classification and confidence
    """
    if not text or not text.strip():
        return {
            "act": "unknown",
            "confidence": 0.0,
            "alternatives": []
        }
    
    text_lower = text.lower().strip()
    
    # Classification patterns
    classifications = []
    
    # Greeting
    greeting_score = score_greeting(text_lower)
    if greeting_score > 0.5:
        classifications.append(("greeting", greeting_score))
    
    # Question
    question_score = score_question(text_lower)
    if question_score > 0.5:
        classifications.append(("question", question_score))
    
    # Request
    request_score = score_request(text_lower)
    if request_score > 0.5:
        classifications.append(("request", request_score))
    
    # Statement
    statement_score = score_statement(text_lower)
    if statement_score > 0.5:
        classifications.append(("statement", statement_score))
    
    # Complaint
    complaint_score = score_complaint(text_lower)
    if complaint_score > 0.5:
        classifications.append(("complaint", complaint_score))
    
    # Apology
    apology_score = score_apology(text_lower)
    if apology_score > 0.5:
        classifications.append(("apology", apology_score))
    
    # If no strong classification, default to statement
    if not classifications:
        classifications.append(("statement", 0.5))
    
    # Sort by score
    classifications.sort(key=lambda x: x[1], reverse=True)
    
    primary_act = classifications[0][0]
    confidence = classifications[0][1]
    alternatives = [{"act": act, "confidence": round(score, 2)} for act, score in classifications[1:4]]
    
    return {
        "act": primary_act,
        "confidence": round(confidence, 2),
        "alternatives": alternatives,
        "text": text
    }

def score_greeting(text: str) -> float:
    """Score likelihood of greeting."""
    greeting_patterns = [
        r'^(hi|hello|hey|greetings|good morning|good afternoon|good evening)',
        r'\b(how are you|how do you do|nice to meet you)\b'
    ]
    
    score = 0.0
    for pattern in greeting_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            score += 0.5
    
    # Check for greeting punctuation
    if text.endswith('!') and len(text.split()) <= 5:
        score += 0.2
    
    return min(1.0, score)

def score_question(text: str) -> float:
    """Score likelihood of question."""
    # Question mark
    if '?' in text:
        score = 0.7
    else:
        score = 0.0
    
    # Question words
    question_words = ['what', 'where', 'when', 'why', 'how', 'who', 'which', 'whose', 'whom']
    question_word_count = sum(1 for word in question_words if word in text)
    score += question_word_count * 0.15
    
    # Question patterns
    question_patterns = [
        r'\b(can you|could you|would you|will you|do you|did you|are you|is it)\b',
        r'\b(what is|what are|how is|how are|where is|where are)\b'
    ]
    
    for pattern in question_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            score += 0.2
    
    return min(1.0, score)

def score_request(text: str) -> float:
    """Score likelihood of request."""
    request_patterns = [
        r'\b(please|kindly|could you|would you|can you)\b',
        r'\b(i want|i need|i would like|i\'d like|help me|show me|tell me)\b',
        r'\b(explain|describe|give me|provide|send)\b'
    ]
    
    score = 0.0
    for pattern in request_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            score += 0.3
    
    # Imperative mood (commands)
    words = text.split()
    if words and words[0].lower() in ['help', 'show', 'tell', 'give', 'explain', 'describe']:
        score += 0.4
    
    return min(1.0, score)

def score_statement(text: str) -> float:
    """Score likelihood of statement."""
    # Default classification if nothing else matches strongly
    if not ('?' in text or text.lower().startswith(('hi', 'hello', 'hey'))):
        return 0.6
    
    # Declarative sentences
    if text.endswith('.') and len(text.split()) > 3:
        return 0.7
    
    return 0.4

def score_complaint(text: str) -> float:
    """Score likelihood of complaint."""
    complaint_indicators = [
        'problem', 'issue', 'wrong', 'error', 'bug', 'broken', 'not working',
        'disappointed', 'frustrated', 'unhappy', 'bad', 'terrible', 'awful'
    ]
    
    score = 0.0
    for indicator in complaint_indicators:
        if indicator in text.lower():
            score += 0.2
    
    return min(1.0, score)

def score_apology(text: str) -> float:
    """Score likelihood of apology."""
    apology_patterns = [
        r'\b(sorry|apologize|apology|excuse me|pardon|forgive)\b',
        r'\b(my bad|my mistake|i was wrong)\b'
    ]
    
    score = 0.0
    for pattern in apology_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            score += 0.5
    
    return min(1.0, score)

def get_appropriate_response(act: str, context: Optional[List[Dict]] = None) -> str:
    """Get appropriate response based on dialogue act."""
    responses = {
        "greeting": "Hello! How can I help you today?",
        "question": "That's a great question! Let me help you with that.",
        "request": "I'd be happy to help with that.",
        "statement": "I understand. Is there anything else you'd like to know?",
        "complaint": "I'm sorry to hear that. Let me help you resolve this.",
        "apology": "No problem at all! How can I assist you?"
    }
    
    return responses.get(act, "How can I help you?")

