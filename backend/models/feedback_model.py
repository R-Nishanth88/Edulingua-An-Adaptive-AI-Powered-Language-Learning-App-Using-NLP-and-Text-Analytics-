from beanie import Document
from beanie import PydanticObjectId
from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import Field

class FeedbackLog(Document):
    user_id: PydanticObjectId
    text: str
    corrections: List[Dict[str, Any]] = Field(default_factory=list)
    suggestions: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "feedback_logs"
        indexes = [
            "user_id",
            "created_at",
        ]