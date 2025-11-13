"""
Grammar Topic Linking Module
Shows mini-lessons when user makes mistakes.
"""
from typing import Dict, List, Optional
from core.ai_service import generate_ai_response, is_ai_available

# Grammar topics knowledge base
GRAMMAR_TOPICS = {
    "articles": {
        "name": "Articles (a, an, the)",
        "description": "Learn when to use 'a', 'an', and 'the'",
        "rules": [
            "Use 'a' before words starting with consonant sounds",
            "Use 'an' before words starting with vowel sounds",
            "Use 'the' for specific or previously mentioned things",
            "Don't use articles with general concepts or plural nouns"
        ],
        "examples": [
            "I need a pen. (any pen)",
            "I need the pen. (specific pen)",
            "She is an engineer. (profession)",
            "I love music. (general, no article)"
        ],
        "common_errors": ["missing_article", "wrong_article", "article_with_plural"]
    },
    "tenses": {
        "name": "Verb Tenses",
        "description": "Understanding past, present, and future tenses",
        "rules": [
            "Present: Use for current actions (I study)",
            "Past: Use for completed actions (I studied)",
            "Future: Use for upcoming actions (I will study)",
            "Match tense to the time of the action"
        ],
        "examples": [
            "I go to school every day. (Present)",
            "I went to school yesterday. (Past)",
            "I will go to school tomorrow. (Future)"
        ],
        "common_errors": ["tense_inconsistency", "wrong_tense", "missing_verb"]
    },
    "prepositions": {
        "name": "Prepositions",
        "description": "Using prepositions correctly (in, on, at, by, with)",
        "rules": [
            "Time: 'in' for months/years, 'on' for days, 'at' for specific times",
            "Place: 'in' for enclosed spaces, 'on' for surfaces, 'at' for points",
            "Common mistakes: 'in home' → 'at home', 'in Monday' → 'on Monday'"
        ],
        "examples": [
            "I live in New York.",
            "The book is on the table.",
            "I'll meet you at 5 PM."
        ],
        "common_errors": ["wrong_preposition", "missing_preposition"]
    },
    "sentence_structure": {
        "name": "Sentence Structure",
        "description": "Correct word order and sentence formation",
        "rules": [
            "English follows Subject-Verb-Object (SVO) order",
            "Always include a subject (except in commands)",
            "Match subject and verb (He goes, not He go)",
            "Put adjectives before nouns"
        ],
        "examples": [
            "My name is John. (Subject + Verb + Complement)",
            "I study English. (Subject + Verb + Object)",
            "What is your name? (Question form)"
        ],
        "common_errors": ["word_order", "missing_subject", "missing_verb", "subject_verb_agreement"]
    },
    "subject_verb_agreement": {
        "name": "Subject-Verb Agreement",
        "description": "Matching subjects and verbs correctly",
        "rules": [
            "Singular subjects need singular verbs (He goes)",
            "Plural subjects need plural verbs (They go)",
            "Third person singular adds 's' (go → goes)",
            "Be careful with 'I', 'you', 'we', 'they' (no 's')"
        ],
        "examples": [
            "He goes to school. (singular)",
            "They go to school. (plural)",
            "I am a student. (first person)"
        ],
        "common_errors": ["subject_verb_agreement", "wrong_verb_form"]
    },
    "punctuation": {
        "name": "Punctuation",
        "description": "Using punctuation marks correctly",
        "rules": [
            "Period (.) ends statements",
            "Question mark (?) ends questions",
            "Comma (,) separates items in lists",
            "Apostrophe (') shows possession or contractions"
        ],
        "examples": [
            "I like apples, bananas, and oranges.",
            "What is your name?",
            "It's John's book."
        ],
        "common_errors": ["missing_punctuation", "wrong_punctuation"]
    }
}

def get_grammar_topic_for_error(error_type: str) -> Optional[Dict]:
    """
    Get grammar topic lesson for a specific error type.
    
    Args:
        error_type: Type of grammar error
    
    Returns:
        Grammar topic dictionary or None
    """
    error_type_lower = error_type.lower()
    
    # Map error types to topics
    error_to_topic = {
        "missing_article": "articles",
        "wrong_article": "articles",
        "article_with_plural": "articles",
        "tense_inconsistency": "tenses",
        "wrong_tense": "tenses",
        "missing_verb": "tenses",
        "wrong_preposition": "prepositions",
        "missing_preposition": "prepositions",
        "word_order": "sentence_structure",
        "missing_subject": "sentence_structure",
        "missing_verb": "sentence_structure",
        "subject_verb_agreement": "subject_verb_agreement",
        "wrong_verb_form": "subject_verb_agreement",
        "punctuation": "punctuation",
        "missing_punctuation": "punctuation",
        "wrong_punctuation": "punctuation"
    }
    
    topic_key = error_to_topic.get(error_type_lower)
    if topic_key and topic_key in GRAMMAR_TOPICS:
        return GRAMMAR_TOPICS[topic_key]
    
    # Try partial matching
    for topic_key, topic_info in GRAMMAR_TOPICS.items():
        if error_type_lower in topic_info.get("common_errors", []):
            return topic_info
    
    return None

def get_mini_lesson_for_errors(errors: List[Dict], use_ai: bool = True) -> Dict:
    """
    Get mini-lessons for the most common errors in a text.
    
    Args:
        errors: List of grammar errors
        use_ai: Whether to use AI for enhanced explanations
    
    Returns:
        Dictionary with recommended lessons and explanations
    """
    if not errors:
        return {
            "lessons": [],
            "message": "No errors found! Great job!"
        }
    
    # Count error types
    error_counts = {}
    for error in errors:
        error_type = error.get("type", "general")
        error_counts[error_type] = error_counts.get(error_type, 0) + 1
    
    # Get top 3 most common errors
    top_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    lessons = []
    for error_type, count in top_errors:
        topic = get_grammar_topic_for_error(error_type)
        if topic:
            lesson = {
                "topic": topic["name"],
                "description": topic["description"],
                "rules": topic["rules"],
                "examples": topic["examples"],
                "error_type": error_type,
                "error_count": count,
                "relevance": "high" if count >= 2 else "medium"
            }
            
            # Add AI-enhanced explanation if available
            if use_ai and is_ai_available():
                try:
                    prompt = f"""Explain this grammar topic in a simple, clear way for a language learner:

Topic: {topic['name']}
Error: {error_type} (appeared {count} time(s))

Provide a brief, encouraging explanation (2-3 sentences):"""
                    
                    ai_explanation = generate_ai_response(
                        prompt,
                        "You are a patient, encouraging grammar teacher explaining concepts simply.",
                        max_tokens=100,
                        temperature=0.6
                    )
                    
                    if ai_explanation:
                        lesson["ai_explanation"] = ai_explanation
                except Exception as e:
                    print(f"⚠️ AI explanation failed: {e}")
            
            lessons.append(lesson)
    
    return {
        "lessons": lessons,
        "total_errors": len(errors),
        "unique_error_types": len(error_counts),
        "message": f"Found {len(errors)} error(s). Here are lessons to help you improve!"
    }

def get_all_grammar_topics() -> List[Dict]:
    """Get all available grammar topics."""
    return [
        {
            "key": key,
            "name": info["name"],
            "description": info["description"],
            "common_errors": info.get("common_errors", [])
        }
        for key, info in GRAMMAR_TOPICS.items()
    ]
