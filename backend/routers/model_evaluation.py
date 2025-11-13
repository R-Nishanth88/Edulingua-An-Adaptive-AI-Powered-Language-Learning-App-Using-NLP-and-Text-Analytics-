"""
Model and Text Analytics Tools Evaluation Router
Endpoints for evaluating NLP models and text analytics tools performance.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from models.user_model import User
from core.auth import get_current_user_optional
from core.model_evaluation import (
    get_model_usage_stats,
    get_text_analytics_tools_stats,
    get_model_performance_comparison,
    get_tool_efficiency_metrics
)

router = APIRouter(prefix="/evaluation/models", tags=["Model Evaluation"])

@router.get("/usage")
async def model_usage_statistics(
    days: int = Query(30, ge=1, le=365),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get usage statistics for all NLP models.
    """
    try:
        result = await get_model_usage_stats(days)
        return result
    except Exception as e:
        print(f"Error getting model usage stats: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to get model usage stats: {str(e)}")

@router.get("/tools")
async def text_analytics_tools_statistics(
    days: int = Query(30, ge=1, le=365),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get performance statistics for text analytics tools.
    """
    try:
        result = await get_text_analytics_tools_stats(days)
        return result
    except Exception as e:
        print(f"Error getting tools stats: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to get tools stats: {str(e)}")

@router.get("/comparison")
async def model_performance_comparison(
    days: int = Query(30, ge=1, le=365),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Compare performance of different models.
    """
    try:
        result = await get_model_performance_comparison(days)
        return result
    except Exception as e:
        print(f"Error comparing models: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to compare models: {str(e)}")

@router.get("/efficiency")
async def tool_efficiency_metrics(
    days: int = Query(30, ge=1, le=365),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get efficiency metrics for text analytics tools.
    """
    try:
        result = await get_tool_efficiency_metrics(days)
        return result
    except Exception as e:
        print(f"Error getting efficiency metrics: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to get efficiency metrics: {str(e)}")

@router.get("/dashboard")
async def model_evaluation_dashboard(
    days: int = Query(30, ge=1, le=365),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get comprehensive model and tools evaluation dashboard.
    """
    try:
        model_usage = await get_model_usage_stats(days)
        tools_stats = await get_text_analytics_tools_stats(days)
        model_comparison = await get_model_performance_comparison(days)
        efficiency = await get_tool_efficiency_metrics(days)
        
        return {
            "period_days": days,
            "model_usage": model_usage,
            "tools_statistics": tools_stats,
            "model_comparison": model_comparison,
            "efficiency_metrics": efficiency,
            "summary": {
                "total_models": model_usage.get("summary", {}).get("total_models", 0),
                "total_tool_categories": tools_stats.get("summary", {}).get("total_tool_categories", 0),
                "overall_success_rate": model_comparison.get("overall_performance", {}).get("average_success_rate", 0),
                "average_efficiency": efficiency.get("summary", {}).get("average_efficiency", 0)
            }
        }
    except Exception as e:
        print(f"Error generating model dashboard: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate dashboard: {str(e)}")

