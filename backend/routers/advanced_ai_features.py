"""
Advanced AI Features Router
Endpoints for context-aware grammar, tone transfer, quality scoring, etc.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from beanie import PydanticObjectId
from models.user_model import User
from core.auth import get_current_user_optional
from core.contextual_grammar import correct_paragraph_with_context, analyze_paragraph_coherence
from core.tone_style_transfer import transfer_tone, get_available_tones, detect_current_tone
from core.writing_quality_score import calculate_writing_quality_score
from core.emotion_intent_analysis import analyze_emotion_and_intent, analyze_emotion, analyze_intent
from core.text_summarizer_reviewer import summarize_and_review
from core.grammar_topic_linking import get_mini_lesson_for_errors, get_all_grammar_topics, get_grammar_topic_for_error
from core.grammar_drills import generate_drill_from_mistakes, generate_grammar_drill
from core.daily_challenges import generate_daily_challenge, get_challenge_categories
from core.grammar_analysis import detect_grammar_errors

router = APIRouter(prefix="/advanced-ai", tags=["Advanced AI Features"])

# Request Models
class ContextualCorrectionRequest(BaseModel):
    text: str
    use_ai: bool = True

class ToneTransferRequest(BaseModel):
    text: str
    target_tone: str  # formal, friendly, academic, creative, concise, casual
    use_ai: bool = True

class QualityScoreRequest(BaseModel):
    text: str
    use_ai: bool = True

class EmotionIntentRequest(BaseModel):
    text: str
    use_ai: bool = True

# Endpoints
@router.post("/contextual-correction")
async def contextual_grammar_correction(
    request: ContextualCorrectionRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Correct grammar errors in paragraphs while preserving context.
    Handles multi-sentence corrections with cross-sentence coherence.
    """
    try:
        if not request.text or len(request.text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Text must be at least 10 characters")
        
        result = correct_paragraph_with_context(request.text, use_ai=request.use_ai)
        return result
    except Exception as e:
        print(f"Error in contextual correction: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Contextual correction failed: {str(e)}")

@router.post("/coherence-analysis")
async def coherence_analysis(
    request: ContextualCorrectionRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Analyze coherence and flow of a paragraph.
    """
    try:
        if not request.text or len(request.text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Text must be at least 10 characters")
        
        result = analyze_paragraph_coherence(request.text)
        return result
    except Exception as e:
        print(f"Error in coherence analysis: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Coherence analysis failed: {str(e)}")

@router.post("/tone-transfer")
async def tone_transfer(
    request: ToneTransferRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Rephrase text into a different tone/style.
    Available tones: formal, friendly, academic, creative, concise, casual
    """
    try:
        if not request.text or len(request.text.strip()) < 5:
            raise HTTPException(status_code=400, detail="Text must be at least 5 characters")
        
        result = transfer_tone(request.text, request.target_tone, use_ai=request.use_ai)
        return result
    except Exception as e:
        print(f"Error in tone transfer: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Tone transfer failed: {str(e)}")

@router.get("/available-tones")
async def get_tones():
    """Get list of available tone styles."""
    return {"tones": get_available_tones()}

@router.post("/detect-tone")
async def detect_tone(
    request: ContextualCorrectionRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Detect the current tone/style of the text.
    """
    try:
        if not request.text or len(request.text.strip()) < 5:
            raise HTTPException(status_code=400, detail="Text must be at least 5 characters")
        
        result = detect_current_tone(request.text)
        return result
    except Exception as e:
        print(f"Error in tone detection: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Tone detection failed: {str(e)}")

@router.post("/quality-score")
async def writing_quality_score(
    request: QualityScoreRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Calculate overall Writing Quality Score (0-100) with detailed breakdown.
    Components: Grammar (30%), Clarity (25%), Coherence (20%), Vocabulary (15%), Tone (10%)
    """
    try:
        if not request.text or len(request.text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Text must be at least 10 characters")
        
        result = calculate_writing_quality_score(request.text, use_ai=request.use_ai)
        return result
    except Exception as e:
        print(f"Error in quality scoring: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Quality scoring failed: {str(e)}")

@router.post("/emotion-intent")
async def emotion_intent_analysis(
    request: EmotionIntentRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Analyze emotional tone and user intent in the text.
    """
    try:
        if not request.text or len(request.text.strip()) < 5:
            raise HTTPException(status_code=400, detail="Text must be at least 5 characters")
        
        result = analyze_emotion_and_intent(request.text, use_ai=request.use_ai)
        return result
    except Exception as e:
        print(f"Error in emotion/intent analysis: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Emotion/intent analysis failed: {str(e)}")

@router.post("/emotion")
async def emotion_analysis(
    request: EmotionIntentRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Detect emotional tone in the text.
    """
    try:
        if not request.text or len(request.text.strip()) < 5:
            raise HTTPException(status_code=400, detail="Text must be at least 5 characters")
        
        result = analyze_emotion(request.text, use_ai=request.use_ai)
        return result
    except Exception as e:
        print(f"Error in emotion analysis: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Emotion analysis failed: {str(e)}")

@router.post("/intent")
async def intent_analysis(
    request: EmotionIntentRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Detect user intent in the text.
    """
    try:
        if not request.text or len(request.text.strip()) < 5:
            raise HTTPException(status_code=400, detail="Text must be at least 5 characters")
        
        result = analyze_intent(request.text, use_ai=request.use_ai)
        return result
    except Exception as e:
        print(f"Error in intent analysis: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Intent analysis failed: {str(e)}")

@router.post("/summarize-review")
async def summarize_and_review_text(
    request: ContextualCorrectionRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Summarize long text and provide improvement points.
    """
    try:
        if not request.text or len(request.text.strip()) < 50:
            raise HTTPException(status_code=400, detail="Text must be at least 50 characters")
        
        result = summarize_and_review(request.text, use_ai=request.use_ai)
        return result
    except Exception as e:
        print(f"Error in summarize/review: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Summarize/review failed: {str(e)}")

@router.post("/grammar-lessons")
async def get_grammar_lessons(
    request: ContextualCorrectionRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get mini-lessons for grammar errors in the text.
    """
    try:
        if not request.text or len(request.text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Text must be at least 10 characters")
        
        errors = detect_grammar_errors(request.text)
        result = get_mini_lesson_for_errors(errors, use_ai=request.use_ai)
        return result
    except Exception as e:
        print(f"Error in grammar lessons: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Grammar lessons failed: {str(e)}")

@router.get("/grammar-topics")
async def get_topics():
    """Get all available grammar topics."""
    return {"topics": get_all_grammar_topics()}

@router.post("/grammar-drill")
async def generate_drill(
    request: ContextualCorrectionRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Generate personalized grammar drill from user's mistakes.
    """
    try:
        if not request.text or len(request.text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Text must be at least 10 characters")
        
        errors = detect_grammar_errors(request.text)
        result = generate_drill_from_mistakes(errors, use_ai=request.use_ai)
        return result
    except Exception as e:
        print(f"Error in grammar drill: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Grammar drill failed: {str(e)}")

@router.post("/grammar-drill/{error_type}")
async def generate_drill_by_type(
    error_type: str,
    request: ContextualCorrectionRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Generate grammar drill for a specific error type.
    """
    try:
        result = generate_grammar_drill(error_type, difficulty="medium", use_ai=request.use_ai)
        return result
    except Exception as e:
        print(f"Error in grammar drill by type: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Grammar drill failed: {str(e)}")

@router.get("/daily-challenge")
async def get_daily_challenge(
    category: Optional[str] = None,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get today's daily writing challenge.
    """
    try:
        user_id = str(current_user.id) if current_user else None
        result = generate_daily_challenge(user_id=user_id, category=category, use_ai=True)
        return result
    except Exception as e:
        print(f"Error in daily challenge: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Daily challenge failed: {str(e)}")

@router.get("/challenge-categories")
async def get_categories():
    """Get all available challenge categories."""
    return {"categories": get_challenge_categories()}

