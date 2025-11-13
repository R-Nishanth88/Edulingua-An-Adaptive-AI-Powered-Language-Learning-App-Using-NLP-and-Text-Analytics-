from typing import List, Dict, Optional
from datetime import datetime, timedelta

def get_recommendations(user_id: str, cefr_level: str, error_types: Optional[List[str]] = None) -> List[Dict]:
    """
    Generate adaptive learning recommendations based on user's level and error patterns.
    """
    recommendations = []
    
    # Base recommendations by CEFR level
    level_recommendations = {
        "A1": [
            {
                "content_title": "Basic Grammar: Articles (a, an, the)",
                "link": "https://learnenglish.britishcouncil.org/grammar/english-grammar-reference/articles",
                "difficulty": "A1",
                "content_type": "article",
                "description": "Learn the basics of using articles in English."
            },
            {
                "content_title": "Essential Vocabulary: Common Words",
                "link": "https://www.ef.com/wwen/english-resources/english-vocabulary/top-3000-words/",
                "difficulty": "A1",
                "content_type": "vocabulary",
                "description": "Build your foundation with the most common English words."
            }
        ],
        "A2": [
            {
                "content_title": "Past Tense Practice",
                "link": "https://learnenglish.britishcouncil.org/grammar/english-grammar-reference/past-tense",
                "difficulty": "A2",
                "content_type": "exercise",
                "description": "Master the past simple and past continuous tenses."
            },
            {
                "content_title": "Daily Conversation Phrases",
                "link": "https://www.fluentu.com/blog/english/english-conversation-practice/",
                "difficulty": "A2",
                "content_type": "article",
                "description": "Practice common phrases for everyday conversations."
            }
        ],
        "B1": [
            {
                "content_title": "Conditional Sentences",
                "link": "https://learnenglish.britishcouncil.org/grammar/english-grammar-reference/conditionals",
                "difficulty": "B1",
                "content_type": "article",
                "description": "Learn to use if-clauses correctly."
            },
            {
                "content_title": "Academic Writing Basics",
                "link": "https://www.oxford-royale.com/articles/academic-writing-tips/",
                "difficulty": "B1",
                "content_type": "article",
                "description": "Improve your formal writing skills."
            }
        ],
        "B2": [
            {
                "content_title": "Advanced Grammar: Subjunctive Mood",
                "link": "https://learnenglish.britishcouncil.org/grammar/english-grammar-reference/subjunctive",
                "difficulty": "B2",
                "content_type": "article",
                "description": "Master advanced grammatical structures."
            },
            {
                "content_title": "Business English Vocabulary",
                "link": "https://www.englishclub.com/business-english/",
                "difficulty": "B2",
                "content_type": "vocabulary",
                "description": "Expand your professional vocabulary."
            }
        ],
        "C1": [
            {
                "content_title": "Advanced Writing Techniques",
                "link": "https://www.cambridgeenglish.org/learning-english/activities-for-learners/",
                "difficulty": "C1",
                "content_type": "article",
                "description": "Refine your writing to near-native level."
            },
            {
                "content_title": "Idioms and Phrasal Verbs",
                "link": "https://www.bbc.co.uk/learningenglish/english/features/the-english-we-speak",
                "difficulty": "C1",
                "content_type": "vocabulary",
                "description": "Learn natural English expressions."
            }
        ],
        "C2": [
            {
                "content_title": "Mastery Level: Nuanced Expression",
                "link": "https://www.cambridgeenglish.org/exams-and-tests/advanced/",
                "difficulty": "C2",
                "content_type": "article",
                "description": "Perfect your command of English."
            }
        ]
    }
    
    # Get base recommendations for user's level
    base_recs = level_recommendations.get(cefr_level, level_recommendations["A1"])
    recommendations.extend(base_recs)
    
    # Add error-specific recommendations
    if error_types:
        error_recommendations = {
            "grammar": {
                "content_title": "Grammar Fundamentals",
                "link": "https://learnenglish.britishcouncil.org/grammar",
                "difficulty": cefr_level,
                "content_type": "article",
                "description": "Focus on improving your grammar accuracy."
            },
            "vocabulary": {
                "content_title": "Vocabulary Building Exercises",
                "link": "https://www.vocabulary.com/",
                "difficulty": cefr_level,
                "content_type": "exercise",
                "description": "Expand your vocabulary range."
            },
            "sentence_structure": {
                "content_title": "Sentence Construction Guide",
                "link": "https://www.grammarly.com/blog/sentence-structure/",
                "difficulty": cefr_level,
                "content_type": "article",
                "description": "Learn to construct clear and effective sentences."
            }
        }
        
        for error_type in error_types[:2]:  # Limit to 2 error-specific recommendations
            if error_type in error_recommendations:
                recommendations.append(error_recommendations[error_type])
    
    # Note: User progress can be fetched separately if needed
    # For now, we'll use error_types passed from the router
    
    return recommendations[:5]  # Return top 5 recommendations
