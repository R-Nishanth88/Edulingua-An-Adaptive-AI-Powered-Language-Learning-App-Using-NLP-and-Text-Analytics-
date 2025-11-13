"""
Adaptive Feedback Engine for personalized grammar learning.
Analyzes user errors and provides targeted learning recommendations.
"""
from typing import List, Dict, Optional
from collections import Counter
from datetime import datetime, timedelta

def generate_feedback(user_id: Optional[str], explanations: List[Dict], error_history: Optional[List[Dict]] = None) -> Dict:
    """
    Generate adaptive feedback based on user's grammar errors.
    
    Args:
        user_id: User identifier (optional)
        explanations: List of error explanations from explanation_engine
        error_history: Historical error data (optional)
    
    Returns:
        Dictionary with feedback, recommendations, and learning tips
    """
    if not explanations:
        return {
            "feedback": "Great job! No major issues detected.",
            "recommendations": [],
            "focus_areas": [],
            "learning_tips": []
        }
    
    # Analyze error types
    error_types = []
    error_categories = []
    
    for exp in explanations:
        error_type = exp.get("type", "general")
        error_types.append(error_type)
        
        if "category" in exp:
            error_categories.append(exp["category"])
    
    # Count error frequencies
    error_counts = Counter(error_types)
    category_counts = Counter(error_categories)
    
    # Generate feedback messages
    feedback_messages = []
    focus_areas = []
    recommendations = []
    learning_tips = []
    
    # Subject-Verb Agreement
    if any("verb" in err.lower() or "subject" in err.lower() for err in error_types):
        feedback_messages.append("Focus on subject-verb agreement.")
        focus_areas.append("Subject-Verb Agreement")
        recommendations.append({
            "topic": "Subject-Verb Agreement",
            "description": "Learn how subjects and verbs must match in number",
            "practice": "Practice with: 'I am', 'You are', 'He/She/It is', 'We/They are'"
        })
        learning_tips.append("Remember: Singular subjects need singular verbs, plural subjects need plural verbs.")
    
    # Articles
    if any("article" in err.lower() for err in error_types):
        feedback_messages.append("Revise the use of articles (a, an, the).")
        focus_areas.append("Articles")
        recommendations.append({
            "topic": "Using Articles",
            "description": "Learn when to use 'a', 'an', and 'the'",
            "practice": "Practice: 'a book' (consonant), 'an apple' (vowel), 'the book' (specific)"
        })
        learning_tips.append("Use 'a' before consonant sounds, 'an' before vowel sounds, 'the' for specific nouns.")
    
    # Word Order
    if any("word_order" in err.lower() or "structure" in err.lower() for err in error_types):
        feedback_messages.append("Work on sentence structure and word order.")
        focus_areas.append("Sentence Structure")
        recommendations.append({
            "topic": "English Word Order",
            "description": "Learn Subject-Verb-Object (SVO) structure",
            "practice": "Practice: 'My name is [name]', 'I like to [verb]'"
        })
        learning_tips.append("English follows Subject-Verb-Object order. Example: 'I eat apples' not 'Eat I apples'.")
    
    # Infinitives
    if any("infinitive" in err.lower() for err in error_types):
        feedback_messages.append("Practice using infinitives (to + verb).")
        focus_areas.append("Infinitives")
        recommendations.append({
            "topic": "Using Infinitives",
            "description": "Learn when to use 'to' before verbs",
            "practice": "After 'like', 'want', 'need': 'I like to play', 'I want to go'"
        })
        learning_tips.append("After verbs like 'like', 'want', 'need', use 'to' + base verb.")
    
    # Punctuation
    if any("punctuation" in err.lower() or "capitalization" in err.lower() for err in error_types):
        feedback_messages.append("Review punctuation and capitalization rules.")
        focus_areas.append("Punctuation & Capitalization")
        recommendations.append({
            "topic": "Punctuation Basics",
            "description": "Learn proper punctuation and capitalization",
            "practice": "Capitalize first letter, end with period/question/exclamation"
        })
        learning_tips.append("Always start sentences with a capital letter and end with proper punctuation.")
    
    # Spelling
    if any("spelling" in err.lower() or "typo" in err.lower() for err in error_types):
        feedback_messages.append("Check spelling carefully.")
        focus_areas.append("Spelling")
        recommendations.append({
            "topic": "Spelling Practice",
            "description": "Improve spelling accuracy",
            "practice": "Use spell-checker and practice common words"
        })
        learning_tips.append("Read more to improve spelling naturally. Use a dictionary for unfamiliar words.")
    
    # Analyze historical patterns if available
    if error_history:
        historical_errors = analyze_error_history(error_history)
        if historical_errors:
            feedback_messages.append(f"Your most common error: {historical_errors['most_common']}")
            focus_areas.extend(historical_errors.get("recurring_areas", []))
    
    # Generate overall feedback
    if feedback_messages:
        feedback = " | ".join(feedback_messages)
    else:
        feedback = "Minor improvements needed. Keep practicing!"
    
    # Calculate progress score
    total_errors = len(error_types)
    unique_error_types = len(set(error_types))
    progress_score = max(0, 100 - (total_errors * 10) - (unique_error_types * 5))
    
    return {
        "feedback": feedback,
        "recommendations": recommendations[:3],  # Top 3 recommendations
        "focus_areas": list(set(focus_areas))[:5],  # Unique focus areas
        "learning_tips": learning_tips[:3],  # Top 3 tips
        "error_summary": {
            "total_errors": total_errors,
            "unique_error_types": unique_error_types,
            "most_common": error_counts.most_common(1)[0][0] if error_counts else None,
            "progress_score": min(100, max(0, progress_score))
        }
    }

def analyze_error_history(error_history: List[Dict]) -> Dict:
    """
    Analyze historical error data to identify patterns.
    
    Args:
        error_history: List of past error records
    
    Returns:
        Dictionary with analysis results
    """
    if not error_history:
        return {}
    
    all_error_types = []
    for record in error_history:
        errors = record.get("errors", [])
        for error in errors:
            error_type = error.get("type", "general")
            all_error_types.append(error_type)
    
    if not all_error_types:
        return {}
    
    error_counts = Counter(all_error_types)
    most_common = error_counts.most_common(1)[0][0] if error_counts else None
    
    # Identify recurring areas
    recurring_areas = []
    if any("article" in err for err in all_error_types):
        recurring_areas.append("Articles")
    if any("verb" in err or "subject" in err for err in all_error_types):
        recurring_areas.append("Subject-Verb Agreement")
    if any("infinitive" in err for err in all_error_types):
        recurring_areas.append("Infinitives")
    
    return {
        "most_common": most_common,
        "recurring_areas": recurring_areas,
        "total_historical_errors": len(all_error_types),
        "error_frequency": dict(error_counts.most_common(5))
    }

def get_personalized_lesson(error_type: str, user_level: str = "A1") -> Dict:
    """
    Get personalized lesson content based on error type and user level.
    
    Args:
        error_type: Type of grammar error
        user_level: User's CEFR level (A1, A2, B1, B2, C1, C2)
    
    Returns:
        Dictionary with lesson content
    """
    lessons = {
        "missing_article": {
            "title": "Using Articles: A, An, The",
            "level": "A1-A2",
            "content": "Articles are words that come before nouns. Use 'a' before consonant sounds, 'an' before vowel sounds, and 'the' for specific nouns.",
            "examples": [
                "I am a student. (consonant sound)",
                "I am an engineer. (vowel sound)",
                "The book is on the table. (specific)"
            ],
            "practice": "Try: 'I am ___ student' → 'I am a student'"
        },
        "missing_infinitive": {
            "title": "Using Infinitives: To + Verb",
            "level": "A2-B1",
            "content": "After certain verbs (like, want, need, try), use 'to' + base verb to form an infinitive.",
            "examples": [
                "I like to play football.",
                "I want to learn English.",
                "I need to study more."
            ],
            "practice": "Try: 'I like play' → 'I like to play'"
        },
        "word_order": {
            "title": "English Sentence Structure",
            "level": "A1",
            "content": "English follows Subject-Verb-Object (SVO) order. The subject comes first, then the verb, then the object.",
            "examples": [
                "My name is John. (Subject: My name, Verb: is, Object: John)",
                "I like apples. (Subject: I, Verb: like, Object: apples)"
            ],
            "practice": "Try: 'name John I' → 'My name is John'"
        }
    }
    
    return lessons.get(error_type, {
        "title": "Grammar Improvement",
        "level": user_level,
        "content": "Keep practicing to improve your grammar!",
        "examples": [],
        "practice": ""
    })

