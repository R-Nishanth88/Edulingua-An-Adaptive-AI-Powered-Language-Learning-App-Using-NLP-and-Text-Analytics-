"""
Adaptive Difficulty Modeling - Adjusts complexity based on user performance.
Uses text analytics to dynamically adjust exercise difficulty.
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from beanie import PydanticObjectId

def calculate_difficulty_score(text: str) -> float:
    """
    Calculate text difficulty score (0-1, where 1 is most difficult).
    
    Args:
        text: Input text
    
    Returns:
        Difficulty score
    """
    from core.readability import calculate_readability
    from core.lexical_semantic import calculate_lexical_diversity
    from core.preprocessing import preprocess_text
    
    # Get text metrics
    preprocessed = preprocess_text(text)
    readability = calculate_readability(text)
    lexical = calculate_lexical_diversity(preprocessed.get("tokens", []))
    
    # Calculate difficulty components
    # 1. Sentence length (longer = harder)
    avg_sentence_length = readability.get("avg_sentence_length", 10)
    sentence_complexity = min(1.0, avg_sentence_length / 25.0)
    
    # 2. Word complexity (longer words = harder)
    words = preprocessed.get("tokens", [])
    avg_word_length = sum(len(w) for w in words) / len(words) if words else 5
    word_complexity = min(1.0, (avg_word_length - 4) / 6.0)
    
    # 3. Lexical diversity (more diverse = harder)
    ttr = lexical.get("ttr", 0.5)
    diversity_complexity = ttr
    
    # 4. Reading ease (lower = harder)
    flesch = readability.get("flesch_reading_ease", 50)
    reading_complexity = 1 - (flesch / 100.0)
    
    # Weighted average
    difficulty = (
        sentence_complexity * 0.3 +
        word_complexity * 0.2 +
        diversity_complexity * 0.2 +
        reading_complexity * 0.3
    )
    
    return round(difficulty, 2)

async def get_user_performance_level(user_id: PydanticObjectId, days: int = 30) -> Dict:
    """
    Get user's current performance level based on recent activity.
    
    Args:
        user_id: User identifier
        days: Number of days to analyze
    
    Returns:
        Dictionary with performance metrics and suggested level
    """
    from models.progress_model import Progress
    from models.grammar_log_model import GrammarLog
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Get recent progress
    recent_progress = await Progress.find(
        Progress.user_id == user_id,
        Progress.date >= cutoff_date
    ).sort(-Progress.date).limit(10).to_list()
    
    # Get recent grammar logs
    recent_logs = await GrammarLog.find(
        GrammarLog.user_id == user_id,
        GrammarLog.timestamp >= cutoff_date
    ).sort(-GrammarLog.timestamp).limit(20).to_list()
    
    # Calculate performance metrics
    avg_error_rate = calculate_avg_error_rate(recent_logs)
    avg_readability = calculate_avg_readability(recent_progress)
    consistency = calculate_consistency(recent_progress)
    
    # Determine suggested level
    suggested_level = determine_level(avg_error_rate, avg_readability, consistency)
    
    return {
        "user_id": str(user_id),
        "current_level": suggested_level,
        "performance_metrics": {
            "avg_error_rate": avg_error_rate,
            "avg_readability": avg_readability,
            "consistency": consistency
        },
        "recommended_difficulty": get_difficulty_for_level(suggested_level),
        "improvement_suggestions": get_improvement_suggestions(avg_error_rate, avg_readability)
    }

def calculate_avg_error_rate(logs: List) -> float:
    """Calculate average error rate."""
    if not logs:
        return 0.5  # Default medium
    
    total_errors = 0
    for log in logs:
        if hasattr(log, 'error_count'):
            total_errors += log.error_count
        elif hasattr(log, 'explanations') and log.explanations:
            total_errors += len(log.explanations)
        else:
            total_errors += 1  # Default to 1 if no error info
    
    total_texts = len(logs)
    
    return round(total_errors / total_texts if total_texts > 0 else 0, 2)

def calculate_avg_readability(progress_list: List) -> float:
    """Calculate average readability score."""
    if not progress_list:
        return 50.0  # Default medium
    
    readability_scores = [p.readability for p in progress_list if hasattr(p, 'readability')]
    return round(sum(readability_scores) / len(readability_scores) if readability_scores else 50.0, 2)

def calculate_consistency(progress_list: List) -> float:
    """Calculate performance consistency (0-1)."""
    if len(progress_list) < 2:
        return 0.5
    
    error_counts = [p.grammar_errors for p in progress_list if hasattr(p, 'grammar_errors')]
    if len(error_counts) < 2:
        return 0.5
    
    # Calculate coefficient of variation (lower = more consistent)
    mean_errors = sum(error_counts) / len(error_counts)
    if mean_errors == 0:
        return 1.0
    
    variance = sum((x - mean_errors) ** 2 for x in error_counts) / len(error_counts)
    std_dev = variance ** 0.5
    cv = std_dev / mean_errors
    
    # Convert to consistency score (0-1)
    consistency = max(0, 1 - min(1, cv))
    return round(consistency, 2)

def determine_level(error_rate: float, readability: float, consistency: float) -> str:
    """
    Determine CEFR level based on performance metrics.
    """
    # Low error rate + high readability + high consistency = higher level
    if error_rate < 0.2 and readability > 70 and consistency > 0.7:
        return "C1"
    elif error_rate < 0.3 and readability > 60 and consistency > 0.6:
        return "B2"
    elif error_rate < 0.4 and readability > 50 and consistency > 0.5:
        return "B1"
    elif error_rate < 0.5 and readability > 40:
        return "A2"
    else:
        return "A1"

def get_difficulty_for_level(level: str) -> Dict:
    """Get difficulty parameters for a CEFR level."""
    difficulties = {
        "A1": {
            "min_sentence_length": 5,
            "max_sentence_length": 10,
            "min_flesch": 80,
            "max_word_length": 6,
            "vocabulary_complexity": "basic"
        },
        "A2": {
            "min_sentence_length": 8,
            "max_sentence_length": 15,
            "min_flesch": 70,
            "max_word_length": 8,
            "vocabulary_complexity": "elementary"
        },
        "B1": {
            "min_sentence_length": 12,
            "max_sentence_length": 20,
            "min_flesch": 60,
            "max_word_length": 10,
            "vocabulary_complexity": "intermediate"
        },
        "B2": {
            "min_sentence_length": 15,
            "max_sentence_length": 25,
            "min_flesch": 50,
            "max_word_length": 12,
            "vocabulary_complexity": "upper_intermediate"
        },
        "C1": {
            "min_sentence_length": 18,
            "max_sentence_length": 30,
            "min_flesch": 40,
            "max_word_length": 15,
            "vocabulary_complexity": "advanced"
        },
        "C2": {
            "min_sentence_length": 20,
            "max_sentence_length": 35,
            "min_flesch": 30,
            "max_word_length": 20,
            "vocabulary_complexity": "proficient"
        }
    }
    
    return difficulties.get(level, difficulties["B1"])

def adjust_text_difficulty(text: str, target_level: str, current_difficulty: float, auto_rephrase: bool = True) -> Dict:
    """
    Adjust text difficulty to match target level.
    
    Args:
        text: Original text
        target_level: Target CEFR level
        current_difficulty: Current difficulty score
        auto_rephrase: If True, automatically rephrase the text
    
    Returns:
        Dictionary with adjusted text and suggestions
    """
    target_params = get_difficulty_for_level(target_level)
    current_score = calculate_difficulty_score(text)
    
    adjustments = []
    rephrased_text = None
    
    # If auto_rephrase is enabled, generate rephrased version
    if auto_rephrase:
        try:
            from core.rephraser import rephrase_text
            from core.ai_service import rephrase_with_ai, is_ai_available
            
            # Try AI rephrasing first for better quality
            if is_ai_available():
                ai_rephrased = rephrase_with_ai(text, style)
                if ai_rephrased and ai_rephrased != text:
                    rephrased_text = ai_rephrased
                    # Calculate difficulty of AI-rephrased version
                    ai_score = calculate_difficulty_score(ai_rephrased)
                    target_score = get_difficulty_score_for_level(target_level)
                    
                    # If AI version is closer to target, use it
                    if abs(ai_score - target_score) < abs(current_score - target_score):
                        result["rephrased_text"] = rephrased_text
                        result["rephrased_difficulty"] = ai_score
                        return result
            
            # Fallback to rule-based rephrasing
            
            # Determine style based on target level
            if target_level in ["A1", "A2"]:
                style = "concise"  # Simpler for beginners
            elif target_level in ["B1", "B2"]:
                style = "fluent"  # Natural for intermediate
            else:
                style = "formal"  # More complex for advanced
            
            # Get rephrased variants
            variants = rephrase_text(text, num_variants=3, style=style)
            
            if variants and len(variants) > 0:
                # Use the first variant as the rephrased text
                rephrased_text = variants[0].get("text", text)
                
                # If we need to simplify (target is easier)
                if current_score > get_difficulty_score_for_level(target_level):
                    # Try to find a simpler variant
                    for variant in variants:
                        variant_text = variant.get("text", "")
                        variant_score = calculate_difficulty_score(variant_text)
                        if variant_score < current_score:
                            rephrased_text = variant_text
                            break
                # If we need to make it harder (target is more difficult)
                elif current_score < get_difficulty_score_for_level(target_level):
                    # Try to find a more complex variant
                    for variant in variants:
                        variant_text = variant.get("text", "")
                        variant_score = calculate_difficulty_score(variant_text)
                        if variant_score > current_score:
                            rephrased_text = variant_text
                            break
        except Exception as e:
            print(f"⚠️ Error in auto-rephrasing: {e}")
            rephrased_text = None
    
    # If too difficult, suggest simplifications
    if current_score > 0.7:
        adjustments.append("Simplify sentence structure")
        adjustments.append("Use shorter words")
        adjustments.append("Break long sentences into shorter ones")
    
    # If too easy, suggest enhancements
    if current_score < 0.3:
        adjustments.append("Use more complex sentence structures")
        adjustments.append("Include advanced vocabulary")
        adjustments.append("Add subordinate clauses")
    
    result = {
        "original_difficulty": current_score,
        "target_level": target_level,
        "target_difficulty": get_difficulty_score_for_level(target_level),
        "adjustments_needed": adjustments,
        "suggested_modifications": generate_difficulty_modifications(text, target_params)
    }
    
    # Add rephrased text if available
    if rephrased_text and rephrased_text != text:
        result["rephrased_text"] = rephrased_text
        result["rephrased_difficulty"] = calculate_difficulty_score(rephrased_text)
    
    return result

def get_difficulty_score_for_level(level: str) -> float:
    """Get expected difficulty score for a level."""
    scores = {
        "A1": 0.2,
        "A2": 0.35,
        "B1": 0.5,
        "B2": 0.65,
        "C1": 0.8,
        "C2": 0.95
    }
    return scores.get(level, 0.5)

def generate_difficulty_modifications(text: str, target_params: Dict) -> List[str]:
    """Generate suggestions to modify text difficulty."""
    suggestions = []
    
    from core.preprocessing import preprocess_text
    preprocessed = preprocess_text(text)
    sentences = preprocessed.get("sentences", [])
    
    avg_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    
    if avg_length > target_params.get("max_sentence_length", 20):
        suggestions.append(f"Break sentences (current avg: {avg_length:.1f} words, target: {target_params['max_sentence_length']})")
    
    if avg_length < target_params.get("min_sentence_length", 10):
        suggestions.append(f"Combine or expand sentences (current avg: {avg_length:.1f} words, target: {target_params['min_sentence_length']})")
    
    return suggestions

def get_improvement_suggestions(error_rate: float, readability: float) -> List[str]:
    """Get suggestions for improvement."""
    suggestions = []
    
    if error_rate > 0.5:
        suggestions.append("Focus on reducing grammar errors through practice")
    
    if readability < 40:
        suggestions.append("Work on improving text clarity and readability")
    
    if error_rate < 0.2 and readability > 70:
        suggestions.append("Great progress! Consider more challenging exercises")
    
    return suggestions

