"""
Evaluation Metrics Router
Endpoints for comprehensive evaluation and analytics.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict
from beanie import PydanticObjectId
from models.user_model import User
from core.auth import get_current_user_optional, get_current_user
from core.evaluation_metrics import (
    calculate_grammar_correction_accuracy,
    calculate_rephrasing_quality,
    calculate_ai_response_quality,
    calculate_learning_effectiveness,
    calculate_user_progress_trends,
    calculate_system_performance_metrics,
    calculate_feature_usage_metrics,
    calculate_quality_metrics,
    generate_comprehensive_evaluation_report
)

router = APIRouter(prefix="/evaluation", tags=["Evaluation Metrics"])

# Request Models
class GrammarAccuracyRequest(BaseModel):
    true_positives: int
    false_positives: int
    false_negatives: int

class RephrasingQualityRequest(BaseModel):
    original_texts: List[str]
    rephrased_texts: List[str]
    user_ratings: Optional[List[int]] = None

class AIQualityRequest(BaseModel):
    response_times: List[float]
    error_rates: List[float]
    user_satisfaction: Optional[List[int]] = None

# Endpoints
@router.post("/grammar-accuracy")
async def grammar_accuracy_metrics(
    request: GrammarAccuracyRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Calculate grammar correction accuracy metrics (Precision, Recall, F1).
    """
    try:
        result = calculate_grammar_correction_accuracy(
            request.true_positives,
            request.false_positives,
            request.false_negatives
        )
        return result
    except Exception as e:
        print(f"Error calculating grammar accuracy: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")

@router.post("/rephrasing-quality")
async def rephrasing_quality_metrics(
    request: RephrasingQualityRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Calculate rephrasing quality metrics.
    """
    try:
        result = calculate_rephrasing_quality(
            request.original_texts,
            request.rephrased_texts,
            request.user_ratings
        )
        return result
    except Exception as e:
        print(f"Error calculating rephrasing quality: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")

@router.post("/ai-quality")
async def ai_quality_metrics(
    request: AIQualityRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Calculate AI service quality metrics.
    """
    try:
        result = calculate_ai_response_quality(
            request.response_times,
            request.error_rates,
            request.user_satisfaction
        )
        return result
    except Exception as e:
        print(f"Error calculating AI quality: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")

@router.get("/learning-effectiveness")
async def learning_effectiveness_metrics(
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Calculate learning effectiveness metrics.
    Returns user-specific metrics if authenticated, otherwise system-wide.
    """
    try:
        user_id = PydanticObjectId(current_user.id) if current_user else None
        result = await calculate_learning_effectiveness(user_id)
        return result
    except Exception as e:
        print(f"Error calculating learning effectiveness: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")

@router.get("/progress-trends")
async def progress_trends(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user)
):
    """
    Calculate user progress trends over time.
    Requires authentication.
    """
    try:
        user_id = PydanticObjectId(current_user.id)
        result = await calculate_user_progress_trends(user_id, days)
        return result
    except Exception as e:
        print(f"Error calculating progress trends: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")

@router.get("/system-performance")
async def system_performance_metrics(
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Calculate overall system performance metrics.
    """
    try:
        result = await calculate_system_performance_metrics()
        return result
    except Exception as e:
        print(f"Error calculating system performance: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")

@router.get("/feature-usage")
async def feature_usage_metrics(
    days: int = Query(30, ge=1, le=365),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Calculate feature usage metrics.
    """
    try:
        result = await calculate_feature_usage_metrics(days)
        return result
    except Exception as e:
        print(f"Error calculating feature usage: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")

@router.get("/quality")
async def quality_metrics(
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Calculate overall quality metrics.
    Returns user-specific metrics if authenticated, otherwise system-wide.
    """
    try:
        user_id = PydanticObjectId(current_user.id) if current_user else None
        result = await calculate_quality_metrics(user_id)
        return result
    except Exception as e:
        print(f"Error calculating quality metrics: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")

@router.get("/comprehensive-report")
async def comprehensive_evaluation_report(
    days: int = Query(30, ge=1, le=365),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Generate comprehensive evaluation report.
    Returns user-specific report if authenticated, otherwise system-wide.
    """
    try:
        user_id = PydanticObjectId(current_user.id) if current_user else None
        result = await generate_comprehensive_evaluation_report(user_id, days)
        return result
    except Exception as e:
        print(f"Error generating comprehensive report: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

@router.get("/dashboard")
async def evaluation_dashboard(
    days: int = Query(30, ge=1, le=365),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get all evaluation metrics for dashboard visualization.
    """
    try:
        user_id = PydanticObjectId(current_user.id) if current_user else None
        
        # Get all metrics
        learning = await calculate_learning_effectiveness(user_id)
        quality = await calculate_quality_metrics(user_id)
        system = await calculate_system_performance_metrics()
        features = await calculate_feature_usage_metrics(days)
        trends = await calculate_user_progress_trends(user_id, days) if user_id else {}
        
        return {
            "learning_effectiveness": learning,
            "quality_metrics": quality,
            "system_performance": system,
            "feature_usage": features,
            "progress_trends": trends,
            "summary": {
                "overall_score": round(
                    (learning.get("error_reduction_rate", 0) * 0.3 +
                     quality.get("quality_score", 0) * 0.3 +
                     system.get("engagement_rate", 0) * 0.2 +
                     (trends.get("improvement_rate", 0) if trends else 50) * 0.2),
                    2
                ),
                "status": "excellent" if learning.get("error_reduction_rate", 0) > 20 else "good"
            }
        }
    except Exception as e:
        print(f"Error generating dashboard metrics: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Dashboard generation failed: {str(e)}")

