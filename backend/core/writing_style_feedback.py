"""
Automatic Feedback on Writing Style.
Scores clarity, conciseness, coherence, formality, and structure.
"""
from typing import Dict, List
import re

def analyze_writing_style(text: str) -> Dict:
    """
    Comprehensive writing style analysis.
    
    Args:
        text: Input text
    
    Returns:
        Dictionary with style scores and feedback
    """
    scores = {
        "clarity": score_clarity(text),
        "conciseness": score_conciseness(text),
        "coherence": score_coherence(text),
        "formality": score_formality(text),
        "structure": score_structure(text)
    }
    
    overall_score = sum(scores.values()) / len(scores)
    
    feedback = generate_style_feedback(scores, text)
    
    return {
        "overall_score": round(overall_score * 100, 1),
        "scores": {k: round(v * 100, 1) for k, v in scores.items()},
        "feedback": feedback,
        "strengths": identify_strengths(scores),
        "improvements": identify_improvements(scores),
        "recommendations": get_style_recommendations(scores)
    }

def score_clarity(text: str) -> float:
    """
    Score text clarity (0-1).
    Higher score = clearer text.
    """
    from core.readability import calculate_readability
    from core.preprocessing import preprocess_text
    
    readability = calculate_readability(text)
    flesch = readability.get("flesch_reading_ease", 50)
    
    # Normalize to 0-1 (Flesch is 0-100)
    clarity_score = flesch / 100.0
    
    # Penalize for passive voice (harder to understand)
    passive_voice_ratio = count_passive_voice(text)
    clarity_score *= (1 - passive_voice_ratio * 0.2)
    
    # Penalize for complex sentences
    avg_sentence_length = readability.get("avg_sentence_length", 10)
    if avg_sentence_length > 20:
        clarity_score *= 0.8
    elif avg_sentence_length > 15:
        clarity_score *= 0.9
    
    return min(1.0, max(0.0, clarity_score))

def score_conciseness(text: str) -> float:
    """
    Score text conciseness (0-1).
    Higher score = more concise.
    """
    from core.preprocessing import preprocess_text
    
    preprocessed = preprocess_text(text)
    words = preprocessed.get("tokens", [])
    sentences = preprocessed.get("sentences", [])
    
    if not words or not sentences:
        return 0.5
    
    # Check for redundancy
    redundancy_score = 1.0 - calculate_redundancy(text)
    
    # Check for wordiness
    wordiness_penalty = count_wordy_phrases(text)
    wordiness_score = max(0.0, 1.0 - (wordiness_penalty * 0.1))
    
    # Average sentence length (shorter = more concise, but not too short)
    avg_length = len(words) / len(sentences) if sentences else 15
    length_score = 1.0 if 10 <= avg_length <= 15 else 0.8 if 8 <= avg_length <= 18 else 0.6
    
    conciseness = (redundancy_score * 0.4 + wordiness_score * 0.3 + length_score * 0.3)
    return min(1.0, max(0.0, conciseness))

def score_coherence(text: str) -> float:
    """
    Score text coherence (0-1).
    Higher score = more coherent.
    """
    try:
        from core.lexical_semantic import analyze_semantic_coherence
        coherence_analysis = analyze_semantic_coherence(text)
        coherence_score = coherence_analysis.get("coherence_score", 0.5)
    except:
        coherence_score = 0.5
    
    # Check for transition words
    transition_words = count_transition_words(text)
    transition_bonus = min(0.2, transition_words * 0.05)
    
    return min(1.0, coherence_score + transition_bonus)

def score_formality(text: str) -> float:
    """
    Score text formality (0-1).
    0 = very informal, 1 = very formal.
    """
    # Informal indicators
    informal_patterns = [
        r'\b(yeah|yep|nope|gonna|wanna|gotta)\b',
        r'\b(like|um|uh|well)\b',  # Filler words
        r'!{2,}',  # Multiple exclamation marks
        r'\b(awesome|cool|nice|great)\b'  # Casual adjectives
    ]
    
    # Formal indicators
    formal_patterns = [
        r'\b(furthermore|moreover|consequently|therefore)\b',
        r'\b(utilize|facilitate|implement|demonstrate)\b',
        r'\b(according to|in accordance with|with regard to)\b',
        r'[A-Z][a-z]+ [A-Z][a-z]+'  # Proper nouns (often formal)
    ]
    
    informal_count = sum(len(re.findall(pattern, text.lower())) for pattern in informal_patterns)
    formal_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in formal_patterns)
    
    total_indicators = informal_count + formal_count
    if total_indicators == 0:
        return 0.5  # Neutral
    
    formality_score = formal_count / total_indicators
    return round(formality_score, 2)

def score_structure(text: str) -> float:
    """
    Score text structure (0-1).
    Higher score = better structure.
    """
    from core.preprocessing import preprocess_text
    
    preprocessed = preprocess_text(text)
    sentences = preprocessed.get("sentences", [])
    
    if not sentences:
        return 0.0
    
    structure_score = 1.0
    
    # Check for proper capitalization
    proper_caps = sum(1 for s in sentences if s and s[0].isupper())
    caps_ratio = proper_caps / len(sentences) if sentences else 0
    structure_score *= (0.5 + caps_ratio * 0.5)
    
    # Check for proper punctuation
    proper_punct = sum(1 for s in sentences if s and s[-1] in '.!?')
    punct_ratio = proper_punct / len(sentences) if sentences else 0
    structure_score *= (0.5 + punct_ratio * 0.5)
    
    # Check for paragraph structure (if multiple sentences)
    if len(sentences) > 3:
        # Good structure has varied sentence lengths
        lengths = [len(s.split()) for s in sentences]
        if lengths:
            length_variance = max(lengths) - min(lengths)
            if length_variance > 5:
                structure_score *= 1.1  # Bonus for variety
    
    return min(1.0, max(0.0, structure_score))

def count_passive_voice(text: str) -> float:
    """Count passive voice ratio."""
    from core.preprocessing import preprocess_text
    
    preprocessed = preprocess_text(text)
    sentences = preprocessed.get("sentences", [])
    
    if not sentences:
        return 0.0
    
    passive_indicators = [
        r'\b(is|are|was|were|been)\s+\w+ed\b',
        r'\b(get|got|gets)\s+\w+ed\b'
    ]
    
    passive_count = 0
    for sentence in sentences:
        for pattern in passive_indicators:
            if re.search(pattern, sentence, re.IGNORECASE):
                passive_count += 1
                break
    
    return passive_count / len(sentences) if sentences else 0.0

def calculate_redundancy(text: str) -> float:
    """Calculate redundancy ratio."""
    from core.preprocessing import preprocess_text
    
    preprocessed = preprocess_text(text)
    words = preprocessed.get("tokens", [])
    
    if len(words) < 2:
        return 0.0
    
    # Count repeated phrases (2-3 word phrases)
    phrase_counts = {}
    for i in range(len(words) - 1):
        phrase = f"{words[i]} {words[i+1]}"
        phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1
    
    repeated_phrases = sum(1 for count in phrase_counts.values() if count > 1)
    redundancy_ratio = repeated_phrases / len(phrase_counts) if phrase_counts else 0.0
    
    return min(1.0, redundancy_ratio)

def count_wordy_phrases(text: str) -> int:
    """Count wordy phrases."""
    wordy_patterns = [
        r'\b(due to the fact that|because of the fact that)\b',
        r'\b(in order to|so as to)\b',
        r'\b(at this point in time|now)\b',
        r'\b(for the purpose of|to)\b',
        r'\b(in the event that|if)\b'
    ]
    
    count = 0
    for pattern in wordy_patterns:
        count += len(re.findall(pattern, text, re.IGNORECASE))
    
    return count

def count_transition_words(text: str) -> int:
    """Count transition words."""
    transitions = [
        'however', 'therefore', 'furthermore', 'moreover', 'consequently',
        'additionally', 'nevertheless', 'meanwhile', 'subsequently', 'thus',
        'hence', 'accordingly', 'alternatively', 'similarly', 'likewise'
    ]
    
    count = 0
    text_lower = text.lower()
    for transition in transitions:
        count += text_lower.count(transition)
    
    return count

def generate_style_feedback(scores: Dict[str, float], text: str) -> Dict:
    """Generate detailed style feedback."""
    feedback = {
        "clarity": get_clarity_feedback(scores["clarity"]),
        "conciseness": get_conciseness_feedback(scores["conciseness"]),
        "coherence": get_coherence_feedback(scores["coherence"]),
        "formality": get_formality_feedback(scores["formality"]),
        "structure": get_structure_feedback(scores["structure"])
    }
    
    return feedback

def get_clarity_feedback(score: float) -> str:
    """Get clarity feedback."""
    if score >= 0.8:
        return "Excellent clarity. Your writing is easy to understand."
    elif score >= 0.6:
        return "Good clarity. Consider simplifying some complex sentences."
    elif score >= 0.4:
        return "Moderate clarity. Try using shorter sentences and simpler words."
    else:
        return "Clarity needs improvement. Use active voice and shorter sentences."

def get_conciseness_feedback(score: float) -> str:
    """Get conciseness feedback."""
    if score >= 0.8:
        return "Very concise writing. You express ideas efficiently."
    elif score >= 0.6:
        return "Generally concise. Look for opportunities to remove redundant words."
    elif score >= 0.4:
        return "Some wordiness detected. Try to be more direct."
    else:
        return "Writing is too wordy. Remove unnecessary words and phrases."

def get_coherence_feedback(score: float) -> str:
    """Get coherence feedback."""
    if score >= 0.8:
        return "Excellent coherence. Ideas flow logically."
    elif score >= 0.6:
        return "Good coherence. Add transition words to improve flow."
    elif score >= 0.4:
        return "Moderate coherence. Use more connecting words between ideas."
    else:
        return "Coherence needs work. Organize ideas more logically."

def get_formality_feedback(score: float) -> str:
    """Get formality feedback."""
    if score >= 0.8:
        return "Very formal tone. Appropriate for academic/professional writing."
    elif score >= 0.6:
        return "Moderately formal. Suitable for most contexts."
    elif score >= 0.4:
        return "Casual tone. Consider more formal language for professional contexts."
    else:
        return "Very informal. Use more formal language for professional writing."

def get_structure_feedback(score: float) -> str:
    """Get structure feedback."""
    if score >= 0.8:
        return "Excellent structure. Sentences are well-formed and varied."
    elif score >= 0.6:
        return "Good structure. Ensure proper capitalization and punctuation."
    elif score >= 0.4:
        return "Structure needs improvement. Check capitalization and punctuation."
    else:
        return "Poor structure. Review sentence formation and punctuation rules."

def identify_strengths(scores: Dict[str, float]) -> List[str]:
    """Identify writing strengths."""
    strengths = []
    for aspect, score in scores.items():
        if score >= 0.7:
            strengths.append(aspect.capitalize())
    return strengths

def identify_improvements(scores: Dict[str, float]) -> List[str]:
    """Identify areas for improvement."""
    improvements = []
    for aspect, score in scores.items():
        if score < 0.6:
            improvements.append(aspect.capitalize())
    return improvements

def get_style_recommendations(scores: Dict[str, float]) -> List[str]:
    """Get style improvement recommendations."""
    recommendations = []
    
    if scores["clarity"] < 0.6:
        recommendations.append("Use active voice instead of passive voice")
        recommendations.append("Break long sentences into shorter ones")
    
    if scores["conciseness"] < 0.6:
        recommendations.append("Remove redundant words and phrases")
        recommendations.append("Avoid wordy expressions like 'due to the fact that'")
    
    if scores["coherence"] < 0.6:
        recommendations.append("Add transition words (however, therefore, furthermore)")
        recommendations.append("Ensure logical flow between sentences")
    
    if scores["formality"] < 0.5:
        recommendations.append("Use more formal vocabulary for professional contexts")
        recommendations.append("Avoid contractions and casual expressions")
    
    if scores["structure"] < 0.6:
        recommendations.append("Ensure proper capitalization and punctuation")
        recommendations.append("Vary sentence lengths for better rhythm")
    
    return recommendations

