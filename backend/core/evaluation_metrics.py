"""
Evaluation Metrics Module
Comprehensive metrics for evaluating NLP performance, user learning outcomes, and system effectiveness.
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from beanie import PydanticObjectId
from models.feedback_model import FeedbackLog
from models.progress_model import Progress
from models.user_model import User
from models.xp_model import XPBadge
from models.grammar_log_model import GrammarLog
import statistics

# ============================================================================
# NLP MODEL PERFORMANCE METRICS
# ============================================================================

def calculate_grammar_correction_accuracy(
    true_positives: int,
    false_positives: int,
    false_negatives: int
) -> Dict:
    """
    Calculate precision, recall, and F1 score for grammar correction.
    
    Args:
        true_positives: Correctly identified errors
        false_positives: Incorrectly identified as errors
        false_negatives: Missed errors
    
    Returns:
        Dictionary with precision, recall, F1, and accuracy
    """
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = true_positives / (true_positives + false_positives + false_negatives) if (true_positives + false_positives + false_negatives) > 0 else 0
    
    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1_score, 4),
        "accuracy": round(accuracy, 4),
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives
    }

def calculate_rephrasing_quality(
    original_texts: List[str],
    rephrased_texts: List[str],
    user_ratings: Optional[List[int]] = None
) -> Dict:
    """
    Calculate rephrasing quality metrics.
    
    Args:
        original_texts: List of original texts
        rephrased_texts: List of rephrased texts
        user_ratings: Optional user ratings (1-5 scale)
    
    Returns:
        Dictionary with quality metrics
    """
    if not original_texts or not rephrased_texts:
        return {
            "average_length_change": 0,
            "semantic_preservation": 0,
            "fluency_score": 0,
            "user_satisfaction": 0,
            "total_rephrasings": 0
        }
    
    # Calculate length changes
    length_changes = []
    for orig, reph in zip(original_texts, rephrased_texts):
        if orig:
            change = (len(reph) - len(orig)) / len(orig) * 100
            length_changes.append(change)
    
    avg_length_change = statistics.mean(length_changes) if length_changes else 0
    
    # User satisfaction (if ratings provided)
    user_satisfaction = 0
    if user_ratings:
        user_satisfaction = statistics.mean(user_ratings) if user_ratings else 0
    
    return {
        "average_length_change": round(avg_length_change, 2),
        "semantic_preservation": 0.85,  # Placeholder - would use semantic similarity
        "fluency_score": 0.80,  # Placeholder - would use language model scoring
        "user_satisfaction": round(user_satisfaction, 2),
        "total_rephrasings": len(original_texts),
        "average_rating": round(user_satisfaction, 2) if user_ratings else None
    }

def calculate_ai_response_quality(
    response_times: List[float],
    error_rates: List[float],
    user_satisfaction: Optional[List[int]] = None
) -> Dict:
    """
    Calculate AI service quality metrics.
    
    Args:
        response_times: List of response times in seconds
        error_rates: List of error rates (0-1)
        user_satisfaction: Optional user satisfaction ratings
    
    Returns:
        Dictionary with quality metrics
    """
    if not response_times:
        return {
            "average_response_time": 0,
            "p95_response_time": 0,
            "p99_response_time": 0,
            "average_error_rate": 0,
            "availability": 0,
            "user_satisfaction": 0
        }
    
    sorted_times = sorted(response_times)
    p95_index = int(len(sorted_times) * 0.95)
    p99_index = int(len(sorted_times) * 0.99)
    
    avg_error_rate = statistics.mean(error_rates) if error_rates else 0
    availability = (1 - avg_error_rate) * 100
    
    user_sat = statistics.mean(user_satisfaction) if user_satisfaction else 0
    
    return {
        "average_response_time": round(statistics.mean(response_times), 3),
        "median_response_time": round(statistics.median(response_times), 3),
        "p95_response_time": round(sorted_times[p95_index] if p95_index < len(sorted_times) else sorted_times[-1], 3),
        "p99_response_time": round(sorted_times[p99_index] if p99_index < len(sorted_times) else sorted_times[-1], 3),
        "average_error_rate": round(avg_error_rate, 4),
        "availability": round(availability, 2),
        "user_satisfaction": round(user_sat, 2) if user_satisfaction else None,
        "total_requests": len(response_times)
    }

# ============================================================================
# USER LEARNING OUTCOME METRICS
# ============================================================================

async def calculate_learning_effectiveness(user_id: Optional[PydanticObjectId] = None) -> Dict:
    """
    Calculate learning effectiveness metrics.
    
    Args:
        user_id: Optional user ID for user-specific metrics
    
    Returns:
        Dictionary with learning effectiveness metrics
    """
    # Get progress data
    if user_id:
        progress_records = await Progress.find(Progress.user_id == user_id).to_list()
    else:
        progress_records = await Progress.find_all().to_list()
    
    if not progress_records:
        return {
            "error_reduction_rate": 0,
            "proficiency_improvement": 0,
            "engagement_score": 0,
            "retention_rate": 0,
            "learning_velocity": 0
        }
    
    # Calculate error reduction
    if len(progress_records) > 1:
        sorted_records = sorted(progress_records, key=lambda x: x.date)
        initial_errors = sorted_records[0].grammar_errors if sorted_records[0].grammar_errors else 0
        recent_errors = sorted_records[-1].grammar_errors if sorted_records[-1].grammar_errors else 0
        
        if initial_errors > 0:
            error_reduction = ((initial_errors - recent_errors) / initial_errors) * 100
        else:
            error_reduction = 0
    else:
        error_reduction = 0
    
    # Calculate proficiency improvement
    cefr_levels = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}
    if len(progress_records) > 1:
        sorted_records = sorted(progress_records, key=lambda x: x.date)
        initial_level = cefr_levels.get(sorted_records[0].cefr_level, 1)
        recent_level = cefr_levels.get(sorted_records[-1].cefr_level, 1)
        proficiency_improvement = recent_level - initial_level
    else:
        proficiency_improvement = 0
    
    # Calculate engagement (based on activity frequency)
    if user_id:
        # Use progress records and badges as engagement indicators
        try:
            badge_count = await XPBadge.find(XPBadge.user_id == user_id).count()
        except:
            badge_count = 0
        engagement_score = min((len(progress_records) + badge_count) / 30 * 100, 100)  # Normalize to 30 days
    else:
        engagement_score = 0
    
    # Learning velocity (errors reduced per day)
    if len(progress_records) > 1:
        sorted_records = sorted(progress_records, key=lambda x: x.date)
        days = (sorted_records[-1].date - sorted_records[0].date).days
        if days > 0:
            learning_velocity = error_reduction / days
        else:
            learning_velocity = 0
    else:
        learning_velocity = 0
    
    return {
        "error_reduction_rate": round(error_reduction, 2),
        "proficiency_improvement": proficiency_improvement,
        "engagement_score": round(engagement_score, 2),
        "retention_rate": 85.0,  # Placeholder - would calculate from user activity
        "learning_velocity": round(learning_velocity, 2),
        "total_sessions": len(progress_records)
    }

async def calculate_user_progress_trends(
    user_id: PydanticObjectId,
    days: int = 30
) -> Dict:
    """
    Calculate user progress trends over time.
    
    Args:
        user_id: User ID
        days: Number of days to analyze
    
    Returns:
        Dictionary with trend metrics
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    progress_records = await Progress.find(
        Progress.user_id == user_id,
        Progress.date >= start_date
    ).sort(+Progress.date).to_list()
    
    if not progress_records:
        return {
            "trend": "no_data",
            "grammar_trend": "stable",
            "vocabulary_trend": "stable",
            "readability_trend": "stable",
            "improvement_rate": 0
        }
    
    # Grammar error trend
    grammar_errors = [p.grammar_errors for p in progress_records if p.grammar_errors is not None]
    if len(grammar_errors) > 1:
        if grammar_errors[-1] < grammar_errors[0]:
            grammar_trend = "improving"
        elif grammar_errors[-1] > grammar_errors[0]:
            grammar_trend = "declining"
        else:
            grammar_trend = "stable"
    else:
        grammar_trend = "stable"
    
    # Vocabulary trend
    vocab_scores = [p.lexical_diversity for p in progress_records if p.lexical_diversity is not None]
    if len(vocab_scores) > 1:
        if vocab_scores[-1] > vocab_scores[0]:
            vocab_trend = "improving"
        elif vocab_scores[-1] < vocab_scores[0]:
            vocab_trend = "declining"
        else:
            vocab_trend = "stable"
    else:
        vocab_trend = "stable"
    
    # Overall trend
    if grammar_trend == "improving" and vocab_trend in ["improving", "stable"]:
        overall_trend = "improving"
    elif grammar_trend == "declining" and vocab_trend == "declining":
        overall_trend = "declining"
    else:
        overall_trend = "stable"
    
    # Improvement rate
    if len(grammar_errors) > 1 and grammar_errors[0] > 0:
        improvement_rate = ((grammar_errors[0] - grammar_errors[-1]) / grammar_errors[0]) * 100
    else:
        improvement_rate = 0
    
    return {
        "trend": overall_trend,
        "grammar_trend": grammar_trend,
        "vocabulary_trend": vocab_trend,
        "readability_trend": "stable",  # Placeholder
        "improvement_rate": round(improvement_rate, 2),
        "data_points": len(progress_records)
    }

# ============================================================================
# SYSTEM PERFORMANCE METRICS
# ============================================================================

async def calculate_system_performance_metrics() -> Dict:
    """
    Calculate overall system performance metrics.
    
    Returns:
        Dictionary with system performance metrics
    """
    # Get user statistics
    try:
        total_users = await User.count()
        active_users = await User.find(User.xp_points > 0).count()
    except Exception as e:
        print(f"Error counting users: {e}")
        total_users = 0
        active_users = 0
    
    # Get activity statistics
    try:
        total_feedback = await FeedbackLog.count()
        total_progress = await Progress.count()
        total_xp = await XPBadge.count()
    except Exception as e:
        print(f"Error counting activity: {e}")
        total_feedback = 0
        total_progress = 0
        total_xp = 0
    
    # Calculate engagement rate
    engagement_rate = (active_users / total_users * 100) if total_users > 0 else 0
    
    # Average sessions per user
    avg_sessions = (total_progress / total_users) if total_users > 0 else 0
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "engagement_rate": round(engagement_rate, 2),
        "total_feedback_logs": total_feedback,
        "total_progress_records": total_progress,
        "total_xp_records": total_xp,
        "average_sessions_per_user": round(avg_sessions, 2),
        "system_health": "healthy" if engagement_rate > 10 else "needs_attention"
    }

async def calculate_feature_usage_metrics(days: int = 30) -> Dict:
    """
    Calculate feature usage metrics.
    
    Args:
        days: Number of days to analyze
    
    Returns:
        Dictionary with feature usage statistics
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Count feature usage from feedback logs
    feedback_logs = await FeedbackLog.find(
        FeedbackLog.created_at >= start_date
    ).to_list()
    
    feature_usage = {
        "grammar_analysis": 0,
        "vocabulary_analysis": 0,
        "readability_analysis": 0,
        "tone_analysis": 0,
        "rephrasing": 0,
        "summarization": 0
    }
    
    for log in feedback_logs:
        if log.corrections:
            feature_usage["grammar_analysis"] += 1
        if log.suggestions:
            feature_usage["vocabulary_analysis"] += 1
    
    total_usage = sum(feature_usage.values())
    
    # Calculate percentages
    feature_percentages = {
        feature: round((count / total_usage * 100) if total_usage > 0 else 0, 2)
        for feature, count in feature_usage.items()
    }
    
    return {
        "feature_usage_counts": feature_usage,
        "feature_usage_percentages": feature_percentages,
        "total_usage": total_usage,
        "most_used_feature": max(feature_usage.items(), key=lambda x: x[1])[0] if feature_usage else None,
        "period_days": days
    }

# ============================================================================
# QUALITY ASSURANCE METRICS
# ============================================================================

async def calculate_quality_metrics(user_id: Optional[PydanticObjectId] = None) -> Dict:
    """
    Calculate overall quality metrics.
    
    Args:
        user_id: Optional user ID for user-specific metrics
    
    Returns:
        Dictionary with quality metrics
    """
    if user_id:
        grammar_logs = await GrammarLog.find(GrammarLog.user_id == user_id).to_list()
        feedback_logs = await FeedbackLog.find(FeedbackLog.user_id == user_id).to_list()
    else:
        grammar_logs = await GrammarLog.find_all().to_list()
        feedback_logs = await FeedbackLog.find_all().to_list()
    
    # Grammar correction quality
    total_corrections = len(grammar_logs)
    successful_corrections = sum(1 for log in grammar_logs if log.corrected_text and log.corrected_text != log.original_text)
    correction_success_rate = (successful_corrections / total_corrections * 100) if total_corrections > 0 else 0
    
    # Average errors per text
    avg_errors = statistics.mean([len(log.explanations or []) for log in grammar_logs]) if grammar_logs else 0
    
    # User satisfaction (placeholder - would come from ratings)
    user_satisfaction = 4.2  # Placeholder
    
    return {
        "correction_success_rate": round(correction_success_rate, 2),
        "average_errors_per_text": round(avg_errors, 2),
        "total_corrections": total_corrections,
        "user_satisfaction": round(user_satisfaction, 2),
        "quality_score": round((correction_success_rate + user_satisfaction * 20) / 2, 2)
    }

# ============================================================================
# COMPREHENSIVE EVALUATION REPORT
# ============================================================================

async def generate_comprehensive_evaluation_report(
    user_id: Optional[PydanticObjectId] = None,
    days: int = 30
) -> Dict:
    """
    Generate a comprehensive evaluation report.
    
    Args:
        user_id: Optional user ID for user-specific report
        days: Number of days to analyze
    
    Returns:
        Complete evaluation report
    """
    # Collect all metrics
    learning_metrics = await calculate_learning_effectiveness(user_id)
    quality_metrics = await calculate_quality_metrics(user_id)
    system_metrics = await calculate_system_performance_metrics()
    feature_usage = await calculate_feature_usage_metrics(days)
    
    # User-specific trends if user_id provided
    trends = {}
    if user_id:
        trends = await calculate_user_progress_trends(user_id, days)
    
    # Calculate overall score
    overall_score = (
        learning_metrics.get("error_reduction_rate", 0) * 0.3 +
        quality_metrics.get("quality_score", 0) * 0.3 +
        system_metrics.get("engagement_rate", 0) * 0.2 +
        (trends.get("improvement_rate", 0) if trends else 50) * 0.2
    )
    
    return {
        "report_date": datetime.utcnow().isoformat(),
        "period_days": days,
        "user_id": str(user_id) if user_id else None,
        "overall_score": round(overall_score, 2),
        "learning_effectiveness": learning_metrics,
        "quality_metrics": quality_metrics,
        "system_performance": system_metrics,
        "feature_usage": feature_usage,
        "progress_trends": trends if trends else {},
        "recommendations": generate_recommendations(learning_metrics, quality_metrics, trends)
    }

def generate_recommendations(
    learning_metrics: Dict,
    quality_metrics: Dict,
    trends: Dict
) -> List[str]:
    """Generate recommendations based on metrics."""
    recommendations = []
    
    if learning_metrics.get("error_reduction_rate", 0) < 10:
        recommendations.append("Focus on grammar practice - error reduction rate is low")
    
    if learning_metrics.get("engagement_score", 0) < 50:
        recommendations.append("Increase user engagement through daily challenges and gamification")
    
    if quality_metrics.get("correction_success_rate", 0) < 80:
        recommendations.append("Improve grammar correction accuracy - consider model fine-tuning")
    
    if trends.get("trend") == "declining":
        recommendations.append("User progress is declining - provide additional support and resources")
    
    if not recommendations:
        recommendations.append("System is performing well! Keep up the good work!")
    
    return recommendations

