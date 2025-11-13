from typing import Dict, List

def explain_correction(original: str, corrected: str, error_type: str) -> Dict:
    """
    Generate human-readable explanation for grammar corrections.
    """
    explanations = {
        "common_mistake": "This is a common mistake. Here's why the correction is better:",
        "grammar": "This correction improves grammatical accuracy:",
        "spelling": "This fixes a spelling error:",
        "punctuation": "Proper punctuation improves clarity:",
        "capitalization": "Capitalization follows English rules:",
        "formatting": "This formatting issue affects readability:"
    }
    
    base_explanation = explanations.get(error_type, "This correction improves your writing:")
    
    # Add specific explanations based on common patterns
    if "your" in original.lower() and "you're" in corrected.lower():
        explanation = f"{base_explanation} 'Your' shows possession (your book), while 'you're' is a contraction of 'you are'."
    elif "its" in original.lower() and "it's" in corrected.lower():
        explanation = f"{base_explanation} 'Its' shows possession (the cat's tail), while 'it's' is a contraction of 'it is'."
    elif "their" in original.lower() or "there" in original.lower():
        explanation = f"{base_explanation} 'Their' shows possession, 'there' refers to a place, and 'they're' means 'they are'."
    else:
        explanation = f"{base_explanation} The corrected version follows standard English grammar rules and improves clarity."
    
    return {
        "original": original,
        "corrected": corrected,
        "error_type": error_type,
        "explanation": explanation,
        "rule": get_grammar_rule(error_type)
    }

def get_grammar_rule(error_type: str) -> str:
    """Return the grammar rule associated with an error type."""
    rules = {
        "common_mistake": "Common mistakes often involve homophones (words that sound the same but have different meanings).",
        "grammar": "Grammar rules ensure that sentences are structured correctly and clearly convey meaning.",
        "spelling": "Correct spelling is essential for clear communication and professionalism.",
        "punctuation": "Punctuation marks help clarify meaning and guide the reader through your text.",
        "capitalization": "Capital letters are used for proper nouns, the start of sentences, and titles.",
        "formatting": "Consistent formatting improves readability and makes your text look professional."
    }
    return rules.get(error_type, "Follow standard English writing conventions.")

def explain_proficiency_prediction(prediction: Dict, features: Dict) -> Dict:
    """
    Explain why a certain proficiency level was predicted.
    """
    level = prediction.get("cefr_level", "A1")
    confidence = prediction.get("confidence", 0.5)
    
    factors = []
    
    grammar_errors = features.get("grammar_errors", 0)
    if grammar_errors == 0:
        factors.append("Excellent grammar accuracy with no detected errors.")
    elif grammar_errors < 3:
        factors.append(f"Good grammar accuracy with only {grammar_errors} minor error(s).")
    else:
        factors.append(f"Grammar accuracy needs improvement ({grammar_errors} errors detected).")
    
    ttr = features.get("ttr", 0.5)
    if ttr > 0.7:
        factors.append("High lexical diversity shows a rich vocabulary.")
    elif ttr > 0.5:
        factors.append("Moderate lexical diversity indicates good vocabulary range.")
    else:
        factors.append("Low lexical diversity suggests limited vocabulary variety.")
    
    flesch_score = features.get("flesch_reading_ease", 50)
    if 30 <= flesch_score <= 50:
        factors.append("Complex text structure indicates advanced writing skills.")
    elif flesch_score > 70:
        factors.append("Simple text structure is appropriate for beginner level.")
    
    return {
        "predicted_level": level,
        "confidence": confidence,
        "factors": factors,
        "recommendations": get_level_recommendations(level)
    }

def get_level_recommendations(level: str) -> List[str]:
    """Get recommendations for improving at a specific level."""
    recommendations = {
        "A1": [
            "Focus on basic vocabulary and simple sentence structures.",
            "Practice common phrases and everyday expressions.",
            "Work on basic grammar rules (articles, present tense)."
        ],
        "A2": [
            "Expand your vocabulary with common words and phrases.",
            "Practice past and future tenses.",
            "Work on sentence variety and length."
        ],
        "B1": [
            "Use more complex sentence structures.",
            "Expand vocabulary with synonyms and varied expressions.",
            "Practice conditional sentences and modal verbs."
        ],
        "B2": [
            "Focus on accuracy and fluency balance.",
            "Use advanced vocabulary and idiomatic expressions.",
            "Practice formal and informal writing styles."
        ],
        "C1": [
            "Refine nuanced expression and subtle meaning.",
            "Master advanced grammatical structures.",
            "Practice sophisticated vocabulary and register."
        ],
        "C2": [
            "Maintain near-native fluency and accuracy.",
            "Focus on stylistic variation and register.",
            "Continue expanding idiomatic knowledge."
        ]
    }
    return recommendations.get(level, ["Continue practicing regularly."])
