from beanie import Document
from beanie import PydanticObjectId
from datetime import datetime
from typing import Optional
from pydantic import Field

class Recommendation(Document):
    user_id: PydanticObjectId
    content_title: str
    link: Optional[str] = None
    difficulty: str = "A1"
    content_type: str = "article"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "recommendations"
        indexes = [
            "user_id",
            "difficulty",
        ]