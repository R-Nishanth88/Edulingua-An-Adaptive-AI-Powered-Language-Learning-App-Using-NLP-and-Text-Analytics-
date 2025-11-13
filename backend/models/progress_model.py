from beanie import Document
from beanie import PydanticObjectId
from datetime import datetime
from typing import Optional
from pydantic import Field

class Progress(Document):
    user_id: PydanticObjectId
    date: datetime = Field(default_factory=datetime.utcnow)
    grammar_errors: int = 0
    readability: float = 0.0
    sentiment: float = 0.0
    cefr_level: str = "A1"
    lexical_diversity: float = 0.0
    
    class Settings:
        name = "progress"
        indexes = [
            "user_id",
            "date",
        ]