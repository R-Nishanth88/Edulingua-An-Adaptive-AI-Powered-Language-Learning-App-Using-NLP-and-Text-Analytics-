from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from beanie import PydanticObjectId
from models.user_model import User
from core.auth import get_current_user_optional
from core.intelligent_chatbot import generate_intelligent_response, analyze_query_intent

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class ChatRequest(BaseModel):
    query: str
    context: Optional[List[Dict]] = None

class ChatResponse(BaseModel):
    response: str
    suggestions: Optional[List[str]] = None
    type: Optional[str] = None

@router.post("/ask", response_model=ChatResponse)
async def chat_with_bot(
    request: ChatRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Intelligent chatbot endpoint for grammar and vocabulary tutoring.
    Uses context-aware responses and can correct sentences.
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Generate intelligent response
        result = generate_intelligent_response(
            query=request.query.strip(),
            context=request.context
        )
        
        return ChatResponse(
            response=result.get("response", "I'm here to help!"),
            suggestions=result.get("suggestions", []),
            type=result.get("type", "general")
        )
    except Exception as e:
        print(f"Chatbot error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")
