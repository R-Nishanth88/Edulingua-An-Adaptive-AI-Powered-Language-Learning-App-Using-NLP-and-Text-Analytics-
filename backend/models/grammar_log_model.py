"""
Grammar Log Model for storing correction history.
"""
from beanie import Document
from datetime import datetime
from typing import List, Dict, Optional
from pydantic import Field
from beanie import PydanticObjectId

class GrammarLog(Document):
    """Model for storing grammar correction logs."""
    user_id: Optional[PydanticObjectId] = None
    original_text: str = Field(..., max_length=1000)
    corrected_text: str = Field(..., max_length=1000)
    error_types: List[str] = Field(default_factory=list)
    error_count: int = 0
    correction_method: str = "rule_based"  # t5_model, rule_based, language_tool
    explanations: List[Dict] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "grammar_logs"
        indexes = [
            "user_id",
            "timestamp",
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "original_text": "i nishanth name",
                "corrected_text": "My name is Nishanth.",
                "error_types": ["word_order", "missing_words"],
                "error_count": 2,
                "correction_method": "rule_based",
                "explanations": [
                    {
                        "type": "word_order",
                        "message": "Sentence structure corrected"
                    }
                ]
            }
        }

