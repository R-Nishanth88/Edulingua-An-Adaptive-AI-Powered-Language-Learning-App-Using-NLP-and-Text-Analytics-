from fastapi import APIRouter, Depends
from typing import Optional, List
from models.user_model import User
from models.recommendation_model import Recommendation
from models.feedback_model import FeedbackLog
from core.auth import get_current_user_optional
from core.recommender import get_recommendations

router = APIRouter(prefix="/recommend", tags=["recommend"])

@router.get("/")
async def get_user_recommendations(
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get adaptive learning recommendations for the user.
    """
    if not current_user:
        # Return general recommendations for non-authenticated users
        return {
            "recommendations": [
                {
                    "content_title": "Getting Started with English",
                    "link": "https://learnenglish.britishcouncil.org/",
                    "difficulty": "A1",
                    "content_type": "article",
                    "description": "Start your English learning journey with basic resources."
                }
            ]
        }
    
    # Get user's recent errors from feedback logs
    recent_logs = await FeedbackLog.find(
        FeedbackLog.user_id == current_user.id
    ).sort(-FeedbackLog.created_at).limit(10).to_list()
    
    error_types = []
    for log in recent_logs:
        corrections = log.corrections if isinstance(log.corrections, list) else []
        for correction in corrections[:3]:
            if isinstance(correction, dict):
                error_types.append(correction.get("type", "grammar"))
    
    # Get recommendations (updated to not require db parameter)
    recommendations = get_recommendations(
        user_id=str(current_user.id),
        cefr_level=current_user.cefr_level,
        error_types=error_types
    )
    
    # Save recommendations to database
    for rec in recommendations:
        existing = await Recommendation.find_one(
            Recommendation.user_id == current_user.id,
            Recommendation.content_title == rec["content_title"]
        )
        
        if not existing:
            db_rec = Recommendation(
                user_id=current_user.id,
                content_title=rec["content_title"],
                link=rec.get("link", ""),
                difficulty=rec.get("difficulty", current_user.cefr_level),
                content_type=rec.get("content_type", "article")
            )
            await db_rec.insert()
    
    return {
        "recommendations": recommendations,
        "user_level": current_user.cefr_level,
        "total_recommendations": len(recommendations)
    }