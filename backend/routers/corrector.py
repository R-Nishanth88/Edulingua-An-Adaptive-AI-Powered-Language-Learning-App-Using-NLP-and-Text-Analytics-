"""
Grammar Correction and Rephrasing Router.
Provides Grammarly++ style grammar correction with explanations and variants.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from core.grammar_corrector import correct_text
from core.rephraser import rephrase_text
from core.explanation_engine import explain_correction
from core.adaptive_feedback import generate_feedback, get_personalized_lesson
from models.grammar_log_model import GrammarLog
from models.user_model import User
from core.auth import get_current_user_optional
from beanie import PydanticObjectId

router = APIRouter(prefix="/grammar", tags=["Grammar Correction"])

class TextInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Text to correct")
    style: Optional[str] = Field(None, description="Rephrasing style: formal, concise, fluent, casual")
    num_variants: int = Field(3, ge=1, le=5, description="Number of rephrased variants")

class GrammarCorrectionResponse(BaseModel):
    original: str
    corrected: str
    rephrased_variants: List[Dict]
    explanations: Dict
    adaptive_feedback: Dict
    correction_method: str
    error_count: int

@router.post("/correct", response_model=GrammarCorrectionResponse)
async def grammar_correction(
    data: TextInput,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Comprehensive grammar correction endpoint.
    
    Takes incorrect or unstructured text and returns:
    - Corrected text
    - Multiple rephrased variants
    - Detailed explanations
    - Adaptive learning feedback
    
    Example:
    ```json
    {
        "text": "name Nishanth I",
        "style": "fluent",
        "num_variants": 3
    }
    ```
    """
    try:
        if not data.text or len(data.text.strip()) < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text must not be empty"
            )
        
        original_text = data.text.strip()
        
        # Step 1: Correct grammar
        correction_result = correct_text(original_text, use_model=True)
        corrected_text = correction_result.get("corrected", original_text)
        correction_method = correction_result.get("method", "none")
        
        # Step 2: Generate rephrased variants
        rephrased_variants = rephrase_text(
            corrected_text,
            num_variants=data.num_variants,
            style=data.style
        )
        
        # Step 3: Generate explanations
        explanations = explain_correction(
            original_text,
            corrected_text,
            detailed=True
        )
        
        # Step 4: Generate adaptive feedback
        user_id = str(current_user.id) if current_user else None
        error_history = None  # Could fetch from database if needed
        
        adaptive_feedback = generate_feedback(
            user_id=user_id,
            explanations=explanations.get("explanations", []),
            error_history=error_history
        )
        
        # Step 5: Extract error types for logging
        error_types = []
        for exp in explanations.get("explanations", []):
            error_type = exp.get("type", "general")
            if error_type not in error_types:
                error_types.append(error_type)
        
        error_count = len(explanations.get("errors", []))
        
        # Step 6: Log correction (if user is authenticated)
        if current_user:
            try:
                grammar_log = GrammarLog(
                    user_id=PydanticObjectId(user_id),
                    original_text=original_text,
                    corrected_text=corrected_text,
                    error_types=error_types,
                    error_count=error_count,
                    correction_method=correction_method,
                    explanations=explanations.get("explanations", [])
                )
                await grammar_log.insert()
            except Exception as e:
                print(f"Error logging grammar correction: {e}")
        
        return {
            "original": original_text,
            "corrected": corrected_text,
            "rephrased_variants": rephrased_variants,
            "explanations": explanations,
            "adaptive_feedback": adaptive_feedback,
            "correction_method": correction_method,
            "error_count": error_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Grammar correction error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Grammar correction failed: {str(e)}"
        )

@router.get("/lesson/{error_type}")
async def get_lesson(
    error_type: str,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get personalized lesson for a specific error type.
    
    Args:
        error_type: Type of grammar error (e.g., "missing_article", "word_order")
    """
    user_level = current_user.cefr_level if current_user else "A1"
    lesson = get_personalized_lesson(error_type, user_level)
    return lesson

@router.get("/history")
async def get_correction_history(
    current_user: User = Depends(get_current_user_optional),
    limit: int = 10
):
    """
    Get user's grammar correction history.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    try:
        user_id = PydanticObjectId(current_user.id)
        logs = await GrammarLog.find(
            GrammarLog.user_id == user_id
        ).sort(-GrammarLog.timestamp).limit(limit).to_list()
        
        return {
            "history": [
                {
                    "original": log.original_text,
                    "corrected": log.corrected_text,
                    "error_types": log.error_types,
                    "error_count": log.error_count,
                    "timestamp": log.timestamp
                }
                for log in logs
            ],
            "total": len(logs)
        }
    except Exception as e:
        print(f"Error fetching history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch correction history"
        )

