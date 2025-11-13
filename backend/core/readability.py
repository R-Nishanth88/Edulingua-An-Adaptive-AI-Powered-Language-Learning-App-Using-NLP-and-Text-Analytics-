import textstat
from typing import Dict
from core.preprocessing import preprocess_text

def calculate_readability(text: str) -> Dict:
    """
    Calculate multiple readability metrics and predict CEFR level.
    """
    if not text or not text.strip():
        return {
            "flesch_reading_ease": 0,
            "flesch_kincaid_grade": 0,
            "gunning_fog": 0,
            "smog_index": 0,
            "cefr_level": "A1",
            "readability_level": "Unknown"
        }
    
    # Calculate readability scores
    flesch_ease = textstat.flesch_reading_ease(text)
    flesch_grade = textstat.flesch_kincaid_grade(text)
    gunning_fog = textstat.gunning_fog(text)
    smog_index = textstat.smog_index(text)
    ari = textstat.automated_readability_index(text)
    
    # Predict CEFR level based on Flesch Reading Ease
    # Flesch Reading Ease: 0-30 (very difficult) = C2, 30-50 = C1, 50-60 = B2, 60-70 = B1, 70-80 = A2, 80-100 = A1
    if flesch_ease >= 80:
        cefr_level = "A1"
        readability_level = "Beginner"
    elif flesch_ease >= 70:
        cefr_level = "A2"
        readability_level = "Elementary"
    elif flesch_ease >= 60:
        cefr_level = "B1"
        readability_level = "Intermediate"
    elif flesch_ease >= 50:
        cefr_level = "B2"
        readability_level = "Upper-Intermediate"
    elif flesch_ease >= 30:
        cefr_level = "C1"
        readability_level = "Advanced"
    else:
        cefr_level = "C2"
        readability_level = "Proficient"
    
    # Analyze sentence complexity
    preprocessed = preprocess_text(text)
    sentences = preprocessed["sentences"]
    tokens = preprocessed["tokens"]
    
    avg_sentence_length = len(tokens) / len(sentences) if sentences else 0
    avg_words_per_sentence = len(tokens) / len(sentences) if sentences else 0
    
    # Identify difficult sentences
    difficult_sentences = []
    for sentence in sentences:
        sentence_ease = textstat.flesch_reading_ease(sentence)
        if sentence_ease < 50:
            difficult_sentences.append({
                "sentence": sentence[:100] + "..." if len(sentence) > 100 else sentence,
                "readability_score": round(sentence_ease, 2),
                "difficulty": "high" if sentence_ease < 30 else "medium"
            })
    
    return {
        "flesch_reading_ease": round(flesch_ease, 2),
        "flesch_kincaid_grade": round(flesch_grade, 2),
        "gunning_fog": round(gunning_fog, 2),
        "smog_index": round(smog_index, 2),
        "ari": round(ari, 2),
        "cefr_level": cefr_level,
        "readability_level": readability_level,
        "avg_sentence_length": round(avg_sentence_length, 2),
        "avg_words_per_sentence": round(avg_words_per_sentence, 2),
        "difficult_sentences": difficult_sentences[:5],
        "interpretation": get_readability_interpretation(flesch_ease)
    }

def get_readability_interpretation(flesch_score: float) -> str:
    """Provide human-readable interpretation of readability score."""
    if flesch_score >= 90:
        return "Very easy to read. Suitable for children."
    elif flesch_score >= 80:
        return "Easy to read. Conversational English."
    elif flesch_score >= 70:
        return "Fairly easy to read. Plain English."
    elif flesch_score >= 60:
        return "Standard. Easily understood by 13-15 year olds."
    elif flesch_score >= 50:
        return "Fairly difficult. College level."
    elif flesch_score >= 30:
        return "Difficult. College graduate level."
    else:
        return "Very difficult. Graduate level."
