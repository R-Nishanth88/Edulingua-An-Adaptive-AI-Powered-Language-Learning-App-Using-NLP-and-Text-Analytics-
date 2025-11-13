"""
Error Pattern Mining - Analytics for tracking common mistakes per user.
Provides personalized improvement paths based on error patterns.
"""
from typing import List, Dict, Optional
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from beanie import PydanticObjectId

async def mine_error_patterns(user_id: PydanticObjectId, days: int = 30) -> Dict:
    """
    Mine error patterns for a specific user.
    
    Args:
        user_id: User identifier
        days: Number of days to analyze
    
    Returns:
        Dictionary with error patterns, frequencies, and recommendations
    """
    from models.feedback_model import FeedbackLog
    from models.grammar_log_model import GrammarLog
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Get all grammar logs for the user
    grammar_logs = await GrammarLog.find(
        GrammarLog.user_id == user_id,
        GrammarLog.timestamp >= cutoff_date
    ).to_list()
    
    # Get feedback logs
    feedback_logs = await FeedbackLog.find(
        FeedbackLog.user_id == user_id,
        FeedbackLog.created_at >= cutoff_date
    ).to_list()
    
    # Aggregate errors
    error_types = []
    error_messages = []
    error_contexts = []
    
    for log in grammar_logs:
        # Extract error types from explanations
        if hasattr(log, 'explanations') and log.explanations:
            for exp in log.explanations:
                if isinstance(exp, dict):
                    error_type = exp.get("type", "unknown")
                    error_types.append(error_type)
                    error_messages.append(exp.get("message", ""))
                    error_contexts.append({
                        "original": log.original_text,
                        "corrected": log.corrected_text,
                        "error_type": error_type
                    })
        # Also check if there's an error_count attribute
        if hasattr(log, 'error_count') and log.error_count > 0:
            # If we have error count but no explanations, use a generic type
            for _ in range(log.error_count):
                error_types.append("general")
    
    for log in feedback_logs:
        if log.corrections:
            for correction in log.corrections:
                if isinstance(correction, dict):
                    error_types.append(correction.get("type", "unknown"))
                    error_messages.append(correction.get("message", ""))
    
    # Count frequencies
    error_type_counts = Counter(error_types)
    error_message_counts = Counter([msg for msg in error_messages if msg])
    
    # Identify patterns
    patterns = identify_error_patterns(error_type_counts, error_contexts)
    
    # Generate recommendations
    recommendations = generate_improvement_path(error_type_counts, patterns)
    
    return {
        "user_id": str(user_id),
        "analysis_period_days": days,
        "total_errors": len(error_types),
        "unique_error_types": len(error_type_counts),
        "most_common_errors": dict(error_type_counts.most_common(10)),
        "error_patterns": patterns,
        "recommendations": recommendations,
        "improvement_areas": get_improvement_areas(error_type_counts),
        "progress_trend": calculate_progress_trend(grammar_logs)
    }

def identify_error_patterns(error_counts: Counter, contexts: List[Dict]) -> List[Dict]:
    """
    Identify patterns in errors.
    """
    patterns = []
    
    # Pattern: Repeated same error type
    for error_type, count in error_counts.most_common(5):
        if count >= 3:
            patterns.append({
                "pattern": "repeated_error",
                "error_type": error_type,
                "frequency": count,
                "severity": "high" if count >= 10 else "medium",
                "description": f"You make '{error_type}' errors frequently ({count} times)"
            })
    
    # Pattern: Error clusters (multiple errors in same text)
    error_clusters = defaultdict(list)
    for context in contexts:
        error_type = context.get("error_type", "")
        if error_type:
            error_clusters[error_type].append(context)
    
    for error_type, cluster in error_clusters.items():
        if len(cluster) >= 3:
            patterns.append({
                "pattern": "error_cluster",
                "error_type": error_type,
                "cluster_size": len(cluster),
                "description": f"Multiple '{error_type}' errors appear together"
            })
    
    # Pattern: Context-specific errors
    context_patterns = analyze_context_patterns(contexts)
    patterns.extend(context_patterns)
    
    return patterns

def analyze_context_patterns(contexts: List[Dict]) -> List[Dict]:
    """Analyze context-specific error patterns."""
    patterns = []
    
    # Group by original text patterns
    text_patterns = defaultdict(list)
    for context in contexts:
        original = context.get("original", "").lower()
        if len(original.split()) <= 5:  # Short phrases
            text_patterns[original].append(context)
    
    for text, contexts_list in text_patterns.items():
        if len(contexts_list) >= 2:
            error_types = [c.get("error_type") for c in contexts_list]
            most_common = Counter(error_types).most_common(1)[0]
            patterns.append({
                "pattern": "context_specific",
                "context": text,
                "error_type": most_common[0],
                "frequency": len(contexts_list),
                "description": f"Errors in similar contexts: '{text}'"
            })
    
    return patterns

def generate_improvement_path(error_counts: Counter, patterns: List[Dict]) -> List[Dict]:
    """
    Generate personalized improvement path based on error patterns.
    """
    recommendations = []
    
    # Prioritize by frequency
    top_errors = error_counts.most_common(5)
    
    for error_type, count in top_errors:
        if count >= 3:
            recommendation = {
                "priority": "high" if count >= 10 else "medium",
                "error_type": error_type,
                "frequency": count,
                "action": get_action_for_error_type(error_type),
                "resources": get_resources_for_error_type(error_type),
                "practice_exercises": get_practice_exercises(error_type)
            }
            recommendations.append(recommendation)
    
    # Add pattern-based recommendations
    for pattern in patterns:
        if pattern["pattern"] == "repeated_error":
            recommendations.append({
                "priority": pattern.get("severity", "medium"),
                "error_type": pattern["error_type"],
                "frequency": pattern["frequency"],
                "action": f"Focus on practicing {pattern['error_type']} corrections",
                "resources": get_resources_for_error_type(pattern["error_type"]),
                "practice_exercises": get_practice_exercises(pattern["error_type"])
            })
    
    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    recommendations.sort(key=lambda x: priority_order.get(x.get("priority", "low"), 2))
    
    return recommendations[:5]  # Top 5 recommendations

def get_action_for_error_type(error_type: str) -> str:
    """Get action recommendation for error type."""
    actions = {
        "word_order": "Practice sentence structure: Subject-Verb-Object order",
        "missing_article": "Review article usage: 'a', 'an', 'the'",
        "missing_infinitive": "Practice infinitives: 'to' + verb after certain verbs",
        "subject_verb_agreement": "Focus on matching subjects and verbs",
        "spelling": "Improve spelling through reading and practice",
        "punctuation": "Review punctuation rules: periods, commas, question marks",
        "capitalization": "Remember to capitalize first letters of sentences"
    }
    return actions.get(error_type, f"Practice {error_type} corrections")

def get_resources_for_error_type(error_type: str) -> List[str]:
    """Get learning resources for error type."""
    resources = {
        "word_order": [
            "English sentence structure guide",
            "Subject-Verb-Object exercises",
            "Word order practice worksheets"
        ],
        "missing_article": [
            "Article usage rules (a/an/the)",
            "Article exercises",
            "Common article mistakes"
        ],
        "missing_infinitive": [
            "Infinitive verb forms",
            "Verbs that take infinitives",
            "Infinitive practice exercises"
        ]
    }
    return resources.get(error_type, [f"{error_type} practice materials"])

def get_practice_exercises(error_type: str) -> List[str]:
    """Get practice exercise suggestions."""
    exercises = {
        "word_order": [
            "Rearrange scrambled sentences",
            "Complete sentences with correct word order",
            "Identify incorrect word order"
        ],
        "missing_article": [
            "Fill in the blanks with articles",
            "Choose correct article",
            "Article usage in context"
        ],
        "missing_infinitive": [
            "Add 'to' where needed",
            "Infinitive vs gerund exercises",
            "Complete sentences with infinitives"
        ]
    }
    return exercises.get(error_type, [f"Practice {error_type} corrections"])

def get_improvement_areas(error_counts: Counter) -> List[Dict]:
    """Get improvement areas based on error frequencies."""
    areas = []
    
    category_mapping = {
        "word_order": "Sentence Structure",
        "missing_article": "Grammar",
        "missing_infinitive": "Grammar",
        "subject_verb_agreement": "Grammar",
        "spelling": "Spelling",
        "punctuation": "Punctuation",
        "capitalization": "Punctuation"
    }
    
    category_counts = defaultdict(int)
    for error_type, count in error_counts.items():
        category = category_mapping.get(error_type, "General")
        category_counts[category] += count
    
    for category, total_count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        areas.append({
            "category": category,
            "error_count": total_count,
            "priority": "high" if total_count >= 20 else "medium" if total_count >= 10 else "low"
        })
    
    return areas

def calculate_progress_trend(logs: List) -> Dict:
    """Calculate progress trend over time."""
    if not logs:
        return {
            "trend": "insufficient_data",
            "improvement_rate": 0
        }
    
    # Group by week
    weekly_errors = defaultdict(int)
    for log in logs:
        week = log.timestamp.isocalendar()[1]  # Week number
        # Get error count from explanations or error_count attribute
        if hasattr(log, 'error_count'):
            error_count = log.error_count
        elif hasattr(log, 'explanations') and log.explanations:
            error_count = len(log.explanations)
        else:
            error_count = 0
        weekly_errors[week] += error_count
    
    if len(weekly_errors) < 2:
        return {
            "trend": "insufficient_data",
            "improvement_rate": 0
        }
    
    # Calculate trend
    weeks = sorted(weekly_errors.keys())
    recent_errors = sum([weekly_errors[w] for w in weeks[-2:]])
    earlier_errors = sum([weekly_errors[w] for w in weeks[:2]]) if len(weeks) >= 2 else recent_errors
    
    if earlier_errors == 0:
        improvement_rate = 0
    else:
        improvement_rate = ((earlier_errors - recent_errors) / earlier_errors) * 100
    
    trend = "improving" if improvement_rate > 0 else "stable" if improvement_rate == 0 else "needs_attention"
    
    return {
        "trend": trend,
        "improvement_rate": round(improvement_rate, 1),
        "recent_errors": recent_errors,
        "earlier_errors": earlier_errors
    }

