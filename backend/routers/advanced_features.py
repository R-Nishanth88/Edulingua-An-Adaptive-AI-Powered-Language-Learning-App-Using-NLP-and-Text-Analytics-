"""
Advanced Features Router - New endpoints for all advanced features.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from beanie import PydanticObjectId

from models.user_model import User
from core.auth import get_current_user, get_current_user_optional
from core.dialog_generation import generate_dialog, generate_response, evaluate_dialog_response
from core.error_pattern_mining import mine_error_patterns
from core.adaptive_difficulty import get_user_performance_level, calculate_difficulty_score, adjust_text_difficulty
from core.writing_style_feedback import analyze_writing_style
from core.semantic_similarity import compare_with_target
from core.essay_scoring import score_essay
from core.dialogue_act_classification import classify_dialogue_act, get_appropriate_response
from core.learning_path import generate_learning_path
from core.plagiarism_detection import detect_plagiarism
from core.lexical_semantic import extract_keywords

router = APIRouter(prefix="/advanced", tags=["Advanced Features"])

# Request Models
class DialogRequest(BaseModel):
    topic: str = Field(..., description="Conversation topic")
    level: str = Field("B1", description="CEFR level")
    num_exchanges: int = Field(5, ge=1, le=10, description="Number of exchanges")

class DialogResponseRequest(BaseModel):
    user_input: str
    context: List[Dict] = Field(default_factory=list)
    topic: str

class SimilarityRequest(BaseModel):
    learner_answer: str
    target_answer: str

class EssayScoringRequest(BaseModel):
    text: str
    topic: Optional[str] = None

class DialogueActRequest(BaseModel):
    text: str
    context: Optional[List[Dict]] = None

class PlagiarismRequest(BaseModel):
    text: str
    reference_texts: Optional[List[str]] = None

# Endpoints
@router.post("/dialog/generate")
async def generate_dialog_endpoint(
    request: DialogRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Generate a conversational dialog for practice."""
    try:
        dialog = generate_dialog(request.topic, request.level, request.num_exchanges)
        return dialog
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating dialog: {str(e)}")

@router.post("/dialog/respond")
async def generate_dialog_response(
    request: DialogResponseRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Generate AI response to user input in a conversation."""
    try:
        response = generate_response(request.user_input, request.context, request.topic)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@router.post("/dialog/evaluate")
async def evaluate_dialog(
    request: Dict,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Evaluate user's dialog response."""
    try:
        result = evaluate_dialog_response(
            request.get("user_response", ""),
            request.get("expected_response", ""),
            request.get("context", [])
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating dialog: {str(e)}")

@router.get("/error-patterns")
async def get_error_patterns(
    days: int = 30,
    current_user: User = Depends(get_current_user)
):
    """Get user's error patterns and improvement recommendations."""
    try:
        patterns = await mine_error_patterns(PydanticObjectId(current_user.id), days)
        return patterns
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error mining patterns: {str(e)}")

@router.get("/performance-level")
async def get_performance_level(
    days: int = 30,
    current_user: User = Depends(get_current_user)
):
    """Get user's current performance level and difficulty recommendations."""
    try:
        level = await get_user_performance_level(PydanticObjectId(current_user.id), days)
        return level
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting performance level: {str(e)}")

@router.post("/difficulty/calculate")
async def calculate_difficulty(
    request: Dict,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Calculate text difficulty score."""
    try:
        score = calculate_difficulty_score(request.get("text", ""))
        return {"difficulty_score": score, "difficulty_level": get_difficulty_level(score)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating difficulty: {str(e)}")

@router.post("/difficulty/adjust")
async def adjust_difficulty(
    request: Dict,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Adjust text difficulty to target level. Automatically rephrases if requested."""
    try:
        auto_rephrase = request.get("auto_rephrase", True)  # Default to True
        result = adjust_text_difficulty(
            request.get("text", ""),
            request.get("target_level", "B1"),
            request.get("current_difficulty", 0.5),
            auto_rephrase=auto_rephrase
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adjusting difficulty: {str(e)}")

@router.post("/style/analyze")
async def analyze_style_endpoint(
    request: Dict,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Analyze writing style (clarity, conciseness, coherence, formality, structure)."""
    try:
        analysis = analyze_writing_style(request.get("text", ""))
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing style: {str(e)}")

@router.post("/similarity/compare")
async def compare_similarity(
    request: SimilarityRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Compare learner's answer with target answer using semantic similarity."""
    try:
        result = compare_with_target(request.learner_answer, request.target_answer)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing similarity: {str(e)}")

@router.post("/essay/score")
async def score_essay_endpoint(
    request: EssayScoringRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Automatically score an essay."""
    try:
        result = score_essay(request.text, request.topic)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scoring essay: {str(e)}")

@router.post("/dialogue/classify")
async def classify_dialogue(
    request: DialogueActRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Classify dialogue act (question, request, greeting, etc.)."""
    try:
        classification = classify_dialogue_act(request.text, request.context)
        response = get_appropriate_response(classification["act"], request.context)
        return {
            **classification,
            "suggested_response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error classifying dialogue: {str(e)}")

@router.get("/learning-path")
async def get_learning_path(
    days: int = 30,
    current_user: User = Depends(get_current_user)
):
    """Get personalized learning path recommendations."""
    try:
        path = await generate_learning_path(PydanticObjectId(current_user.id), days)
        return path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating learning path: {str(e)}")

@router.post("/plagiarism/check")
async def check_plagiarism(
    request: PlagiarismRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Check text for plagiarism and repetition."""
    try:
        result = detect_plagiarism(request.text, request.reference_texts)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking plagiarism: {str(e)}")

@router.post("/keywords/extract")
async def extract_keywords_endpoint(
    request: Dict,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Extract keywords from text for revision notes."""
    try:
        keywords = extract_keywords(request.get("text", ""), top_n=request.get("top_n", 10))
        return {
            "keywords": keywords,
            "count": len(keywords)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting keywords: {str(e)}")

def get_difficulty_level(score: float) -> str:
    """Get difficulty level from score."""
    if score >= 0.8:
        return "Very Difficult"
    elif score >= 0.6:
        return "Difficult"
    elif score >= 0.4:
        return "Moderate"
    elif score >= 0.2:
        return "Easy"
    else:
        return "Very Easy"

