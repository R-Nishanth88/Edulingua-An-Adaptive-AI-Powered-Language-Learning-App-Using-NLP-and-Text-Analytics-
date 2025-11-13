from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from datetime import datetime, timedelta
from models.user_model import User
from models.progress_model import Progress
from models.feedback_model import FeedbackLog
from core.auth import get_current_user
from core.error_mining import mine_common_errors

router = APIRouter(prefix="/progress", tags=["progress"])

@router.get("/")
async def get_user_progress(
    days: int = 30,
    current_user: User = Depends(get_current_user)
):
    """
    Get user progress data for visualization.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Get progress data for the last N days
    start_date = datetime.utcnow() - timedelta(days=days)
    progress_records = await Progress.find(
        Progress.user_id == current_user.id,
        Progress.date >= start_date
    ).sort(+Progress.date).to_list()
    
    # Get feedback logs for error mining
    feedback_logs = await FeedbackLog.find(
        FeedbackLog.user_id == current_user.id,
        FeedbackLog.created_at >= start_date
    ).to_list()
    
    # Format progress data for charts
    grammar_trend = [
        {
            "date": record.date.isoformat() if record.date else None,
            "errors": record.grammar_errors,
            "cefr_level": record.cefr_level
        }
        for record in progress_records
    ]
    
    readability_trend = [
        {
            "date": record.date.isoformat() if record.date else None,
            "readability": record.readability,
            "cefr_level": record.cefr_level
        }
        for record in progress_records
    ]
    
    sentiment_trend = [
        {
            "date": record.date.isoformat() if record.date else None,
            "sentiment": record.sentiment
        }
        for record in progress_records
    ]
    
    # Error mining
    error_analysis = mine_common_errors([
        {
            "corrections": log.corrections if isinstance(log.corrections, list) else []
        }
        for log in feedback_logs
    ])
    
    # Calculate statistics
    total_practices = len(progress_records)
    avg_errors = sum(r.grammar_errors for r in progress_records) / total_practices if total_practices > 0 else 0
    current_level = progress_records[-1].cefr_level if progress_records else current_user.cefr_level
    
    return {
        "user": {
            "username": current_user.username,
            "current_cefr_level": current_level,
            "xp_points": current_user.xp_points,
            "total_practices": total_practices
        },
        "trends": {
            "grammar_errors": grammar_trend,
            "readability": readability_trend,
            "sentiment": sentiment_trend
        },
        "statistics": {
            "average_errors": round(avg_errors, 2),
            "total_practices": total_practices,
            "improvement_rate": calculate_improvement_rate(progress_records)
        },
        "error_analysis": error_analysis
    }

def calculate_improvement_rate(progress_records):
    """Calculate improvement rate based on error reduction."""
    if len(progress_records) < 2:
        return 0.0
    
    first_half = progress_records[:len(progress_records)//2]
    second_half = progress_records[len(progress_records)//2:]
    
    avg_first = sum(r.grammar_errors for r in first_half) / len(first_half) if first_half else 0
    avg_second = sum(r.grammar_errors for r in second_half) / len(second_half) if second_half else 0
    
    if avg_first == 0:
        return 100.0 if avg_second == 0 else 0.0
    
    improvement = ((avg_first - avg_second) / avg_first) * 100
    return round(improvement, 2)