"""
Automatic Essay Scoring - Grades essays using coherence, grammar, vocabulary, and argument strength.
"""
from typing import Dict, List, Optional
from datetime import datetime

def score_essay(text: str, topic: Optional[str] = None) -> Dict:
    """
    Comprehensive essay scoring.
    
    Args:
        text: Essay text
        topic: Essay topic (optional)
    
    Returns:
        Dictionary with scores and detailed feedback
    """
    from core.grammar_analysis import detect_grammar_errors
    from core.readability import calculate_readability
    from core.lexical_semantic import calculate_lexical_diversity, analyze_semantic_coherence
    from core.writing_style_feedback import analyze_writing_style
    from core.preprocessing import preprocess_text
    
    # Calculate component scores
    preprocessed = preprocess_text(text)
    grammar_errors = detect_grammar_errors(text)
    readability = calculate_readability(text)
    lexical = calculate_lexical_diversity(preprocessed.get("tokens", []))
    
    # Get coherence analysis
    try:
        from core.lexical_semantic import analyze_semantic_coherence
        coherence = analyze_semantic_coherence(text)
    except:
        coherence = {"coherence_score": 0.5, "topic_consistency": "medium"}
    
    style = analyze_writing_style(text)
    
    # Component scores (0-100)
    grammar_score = calculate_grammar_score(grammar_errors, len(preprocessed.get("tokens", [])))
    vocabulary_score = calculate_vocabulary_score(lexical, preprocessed)
    coherence_score = calculate_coherence_score(coherence, text)
    structure_score = calculate_structure_score(text, preprocessed)
    argument_score = calculate_argument_strength(text, topic)
    style_score = style.get("overall_score", 50)
    
    # Weighted overall score
    overall_score = (
        grammar_score * 0.25 +
        vocabulary_score * 0.20 +
        coherence_score * 0.20 +
        structure_score * 0.15 +
        argument_score * 0.10 +
        style_score * 0.10
    )
    
    # Determine grade
    grade = get_grade(overall_score)
    
    # Generate feedback
    feedback = generate_essay_feedback({
        "grammar": grammar_score,
        "vocabulary": vocabulary_score,
        "coherence": coherence_score,
        "structure": structure_score,
        "argument": argument_score,
        "style": style_score
    })
    
    return {
        "overall_score": round(overall_score, 1),
        "grade": grade,
        "component_scores": {
            "grammar": round(grammar_score, 1),
            "vocabulary": round(vocabulary_score, 1),
            "coherence": round(coherence_score, 1),
            "structure": round(structure_score, 1),
            "argument_strength": round(argument_score, 1),
            "style": round(style_score, 1)
        },
        "feedback": feedback,
        "strengths": identify_essay_strengths({
            "grammar": grammar_score,
            "vocabulary": vocabulary_score,
            "coherence": coherence_score,
            "structure": structure_score,
            "argument": argument_score
        }),
        "improvements": identify_essay_improvements({
            "grammar": grammar_score,
            "vocabulary": vocabulary_score,
            "coherence": coherence_score,
            "structure": structure_score,
            "argument": argument_score
        }),
        "detailed_analysis": {
            "word_count": preprocessed.get("word_count", 0),
            "sentence_count": preprocessed.get("sentence_count", 0),
            "grammar_errors": len(grammar_errors),
            "readability": readability.get("flesch_reading_ease", 50),
            "lexical_diversity": lexical.get("ttr", 0.5)
        }
    }

def calculate_grammar_score(errors: List[Dict], word_count: int) -> float:
    """Calculate grammar score (0-100)."""
    if word_count == 0:
        return 0.0
    
    error_rate = len(errors) / word_count
    # Lower error rate = higher score
    score = max(0, 100 - (error_rate * 1000))  # Scale appropriately
    return min(100, score)

def calculate_vocabulary_score(lexical: Dict, preprocessed: Dict) -> float:
    """Calculate vocabulary score (0-100)."""
    ttr = lexical.get("ttr", 0.5)
    unique_words = lexical.get("unique_words", 0)
    total_words = lexical.get("total_words", 0)
    
    # Diversity score (0-50)
    diversity_score = ttr * 50
    
    # Range score (0-50) - more unique words = better
    if total_words > 0:
        range_score = min(50, (unique_words / total_words) * 50)
    else:
        range_score = 0
    
    return diversity_score + range_score

def calculate_coherence_score(coherence: Dict, text: str) -> float:
    """Calculate coherence score (0-100)."""
    coherence_score = coherence.get("coherence_score", 0.5)
    base_score = coherence_score * 100
    
    # Bonus for transition words
    from core.writing_style_feedback import count_transition_words
    transitions = count_transition_words(text)
    transition_bonus = min(10, transitions * 2)
    
    return min(100, base_score + transition_bonus)

def calculate_structure_score(text: str, preprocessed: Dict) -> float:
    """Calculate structure score (0-100)."""
    sentences = preprocessed.get("sentences", [])
    
    if not sentences:
        return 0.0
    
    score = 100.0
    
    # Penalize for very short or very long essays
    word_count = preprocessed.get("word_count", 0)
    if word_count < 100:
        score -= 20  # Too short
    elif word_count < 200:
        score -= 10  # A bit short
    
    # Check paragraph structure (simplified)
    if len(sentences) < 3:
        score -= 15  # Too few sentences
    
    # Check for proper formatting
    proper_caps = sum(1 for s in sentences if s and s[0].isupper())
    caps_ratio = proper_caps / len(sentences) if sentences else 0
    score *= (0.5 + caps_ratio * 0.5)
    
    return max(0, min(100, score))

def calculate_argument_strength(text: str, topic: Optional[str] = None) -> float:
    """Calculate argument strength (0-100)."""
    from core.preprocessing import preprocess_text
    
    preprocessed = preprocess_text(text)
    sentences = preprocessed.get("sentences", [])
    
    if not sentences:
        return 0.0
    
    score = 50.0  # Base score
    
    # Check for argumentative language
    argument_indicators = [
        "because", "therefore", "however", "furthermore", "moreover",
        "consequently", "thus", "hence", "evidence", "support", "prove",
        "demonstrate", "indicate", "suggest", "argue", "claim"
    ]
    
    text_lower = text.lower()
    indicator_count = sum(1 for indicator in argument_indicators if indicator in text_lower)
    score += min(30, indicator_count * 5)
    
    # Check for examples or evidence
    example_indicators = ["for example", "for instance", "such as", "like", "including"]
    example_count = sum(1 for indicator in example_indicators if indicator in text_lower)
    score += min(20, example_count * 5)
    
    # Length bonus (longer essays can develop arguments better)
    word_count = preprocessed.get("word_count", 0)
    if word_count > 300:
        score += 10
    elif word_count > 200:
        score += 5
    
    return min(100, max(0, score))

def get_grade(score: float) -> str:
    """Convert score to letter grade."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

def generate_essay_feedback(scores: Dict[str, float]) -> Dict:
    """Generate detailed essay feedback."""
    feedback = {
        "grammar": get_component_feedback("grammar", scores["grammar"]),
        "vocabulary": get_component_feedback("vocabulary", scores["vocabulary"]),
        "coherence": get_component_feedback("coherence", scores["coherence"]),
        "structure": get_component_feedback("structure", scores["structure"]),
        "argument": get_component_feedback("argument", scores["argument"])
    }
    
    return feedback

def get_component_feedback(component: str, score: float) -> str:
    """Get feedback for a component."""
    if score >= 80:
        return f"Excellent {component}. Keep up the good work!"
    elif score >= 70:
        return f"Good {component}. Minor improvements could be made."
    elif score >= 60:
        return f"Fair {component}. Focus on this area for improvement."
    else:
        return f"{component.capitalize()} needs significant improvement. Practice more in this area."

def identify_essay_strengths(scores: Dict[str, float]) -> List[str]:
    """Identify essay strengths."""
    strengths = []
    for component, score in scores.items():
        if score >= 75:
            strengths.append(component.capitalize())
    return strengths

def identify_essay_improvements(scores: Dict[str, float]) -> List[str]:
    """Identify areas for improvement."""
    improvements = []
    for component, score in scores.items():
        if score < 70:
            improvements.append(component.capitalize())
    return improvements

