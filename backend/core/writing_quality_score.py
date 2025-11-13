"""
AI Feedback Scoring Module
Provides overall Writing Quality Score (0-100) considering fluency, clarity, and coherence.
"""
from typing import Dict, Optional
from core.grammar_analysis import detect_grammar_errors, correct_grammar
from core.readability import calculate_readability
from core.lexical_semantic import calculate_lexical_diversity, analyze_semantic_coherence
from core.tone_style import analyze_tone_and_style
from core.contextual_grammar import analyze_paragraph_coherence

def calculate_writing_quality_score(text: str, use_ai: bool = True) -> Dict:
    """
    Calculate overall Writing Quality Score (0-100) with detailed breakdown.
    
    Scoring Components:
    - Grammar & Correctness (30%): Grammar errors, spelling, punctuation
    - Clarity & Readability (25%): Readability scores, sentence structure
    - Coherence & Flow (20%): Semantic coherence, paragraph flow
    - Vocabulary & Style (15%): Lexical diversity, word choice
    - Tone & Appropriateness (10%): Tone consistency, formality
    
    Args:
        text: Input text to score
        use_ai: Whether to use AI for enhanced scoring
    
    Returns:
        Dictionary with overall score, component scores, and feedback
    """
    if not text or not text.strip():
        return {
            "overall_score": 0,
            "components": {},
            "feedback": "Text is empty",
            "grade": "F"
        }
    
    # 1. Grammar & Correctness (30%)
    grammar_errors = detect_grammar_errors(text)
    error_count = len(grammar_errors)
    word_count = len(text.split())
    error_rate = min(error_count / max(word_count, 1), 1.0)  # Normalize to 0-1
    grammar_score = max(0, (1 - error_rate) * 100)  # Higher error rate = lower score
    
    # 2. Clarity & Readability (25%)
    try:
        readability = calculate_readability(text)
        flesch_score = readability.get("flesch_reading_ease", 50)
        # Flesch score: 0-30 (very difficult) to 90-100 (very easy)
        # For writing quality, we want moderate difficulty (50-70 is good)
        # Adjust: 50-70 range gets high score
        if 50 <= flesch_score <= 70:
            readability_score = 100
        elif 30 <= flesch_score < 50:
            readability_score = 70 + (flesch_score - 30) * 1.5  # 70-100
        elif 70 < flesch_score <= 90:
            readability_score = 100 - (flesch_score - 70) * 1.5  # 100-70
        else:
            readability_score = max(0, 100 - abs(flesch_score - 60) * 2)
        readability_score = max(0, min(100, readability_score))
    except:
        readability_score = 50  # Default if calculation fails
    
    # 3. Coherence & Flow (20%)
    try:
        coherence = analyze_semantic_coherence(text)
        coherence_score = coherence.get("coherence_score", 0.5) * 100
        
        # Also check paragraph coherence if multiple sentences
        if len(text.split('.')) > 1:
            para_coherence = analyze_paragraph_coherence(text)
            para_score = para_coherence.get("coherence_score", 0.5) * 100
            coherence_score = (coherence_score + para_score) / 2
    except:
        coherence_score = 50
    
    # 4. Vocabulary & Style (15%)
    try:
        tokens = text.split()
        lexical = calculate_lexical_diversity(tokens)
        ttr = lexical.get("ttr", 0.5)  # Type-Token Ratio (0-1)
        # Higher TTR = more diverse vocabulary = better
        vocabulary_score = ttr * 100
    except:
        vocabulary_score = 50
    
    # 5. Tone & Appropriateness (10%)
    try:
        tone_style = analyze_tone_and_style(text)
        # Check if tone is appropriate and consistent
        # For now, give score based on sentiment polarity (neutral to positive is good)
        sentiment = tone_style.get("sentiment", {}).get("polarity", 0)
        tone_score = 50 + (sentiment * 50)  # -1 to 1 maps to 0-100
        tone_score = max(0, min(100, tone_score))
    except:
        tone_score = 50
    
    # Calculate weighted overall score
    overall_score = (
        grammar_score * 0.30 +
        readability_score * 0.25 +
        coherence_score * 0.20 +
        vocabulary_score * 0.15 +
        tone_score * 0.10
    )
    
    # Round to 1 decimal
    overall_score = round(overall_score, 1)
    
    # Get grade
    if overall_score >= 90:
        grade = "A+"
    elif overall_score >= 80:
        grade = "A"
    elif overall_score >= 70:
        grade = "B"
    elif overall_score >= 60:
        grade = "C"
    elif overall_score >= 50:
        grade = "D"
    else:
        grade = "F"
    
    # Generate feedback
    feedback = generate_quality_feedback(
        overall_score,
        grammar_score,
        readability_score,
        coherence_score,
        vocabulary_score,
        tone_score,
        error_count
    )
    
    # AI-enhanced feedback if available
    ai_feedback = None
    if use_ai:
        try:
            from core.ai_service import generate_ai_response, is_ai_available
            if is_ai_available():
                prompt = f"""Provide constructive feedback on this writing sample (Score: {overall_score}/100):

Text: {text}

Give 2-3 specific, actionable suggestions for improvement. Focus on the weakest areas."""
                
                ai_feedback = generate_ai_response(
                    prompt,
                    "You are a writing tutor providing constructive feedback. Be specific and encouraging.",
                    max_tokens=200,
                    temperature=0.6
                )
        except Exception as e:
            print(f"⚠️ AI feedback generation failed: {e}")
    
    return {
        "overall_score": overall_score,
        "grade": grade,
        "components": {
            "grammar_correctness": {
                "score": round(grammar_score, 1),
                "weight": 0.30,
                "errors_found": error_count
            },
            "clarity_readability": {
                "score": round(readability_score, 1),
                "weight": 0.25,
                "flesch_reading_ease": readability.get("flesch_reading_ease", 0) if 'readability' in locals() else 0
            },
            "coherence_flow": {
                "score": round(coherence_score, 1),
                "weight": 0.20
            },
            "vocabulary_style": {
                "score": round(vocabulary_score, 1),
                "weight": 0.15,
                "lexical_diversity": lexical.get("ttr", 0) if 'lexical' in locals() else 0
            },
            "tone_appropriateness": {
                "score": round(tone_score, 1),
                "weight": 0.10
            }
        },
        "feedback": feedback,
        "ai_feedback": ai_feedback,
        "word_count": word_count,
        "sentence_count": len([s for s in text.split('.') if s.strip()])
    }

def generate_quality_feedback(
    overall_score: float,
    grammar_score: float,
    readability_score: float,
    coherence_score: float,
    vocabulary_score: float,
    tone_score: float,
    error_count: int
) -> str:
    """Generate human-readable feedback based on scores."""
    feedback_parts = []
    
    # Overall assessment
    if overall_score >= 90:
        feedback_parts.append("Excellent writing! Your text demonstrates strong grammar, clarity, and coherence.")
    elif overall_score >= 80:
        feedback_parts.append("Good writing with minor areas for improvement.")
    elif overall_score >= 70:
        feedback_parts.append("Decent writing, but there's room for improvement in several areas.")
    else:
        feedback_parts.append("Your writing needs improvement. Focus on the areas below.")
    
    # Specific feedback
    if grammar_score < 70:
        feedback_parts.append(f"Grammar: Fix {error_count} error(s) to improve correctness.")
    
    if readability_score < 70:
        feedback_parts.append("Clarity: Simplify sentence structure and improve readability.")
    
    if coherence_score < 70:
        feedback_parts.append("Coherence: Improve logical flow and connections between ideas.")
    
    if vocabulary_score < 70:
        feedback_parts.append("Vocabulary: Use more diverse and precise word choices.")
    
    if tone_score < 70:
        feedback_parts.append("Tone: Ensure consistent and appropriate tone throughout.")
    
    # Positive reinforcement
    strengths = []
    if grammar_score >= 80:
        strengths.append("strong grammar")
    if readability_score >= 80:
        strengths.append("clear writing")
    if coherence_score >= 80:
        strengths.append("good flow")
    if vocabulary_score >= 80:
        strengths.append("rich vocabulary")
    
    if strengths:
        feedback_parts.append(f"Your strengths: {', '.join(strengths)}.")
    
    return " ".join(feedback_parts)

