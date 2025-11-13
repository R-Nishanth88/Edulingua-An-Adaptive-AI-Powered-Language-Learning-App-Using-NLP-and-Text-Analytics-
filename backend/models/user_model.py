from beanie import Document
from datetime import datetime
from typing import Optional
from pydantic import Field, EmailStr

class User(Document):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str
    cefr_level: str = "A1"
    xp_points: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"
        indexes = [
            "username",
            "email",
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "cefr_level": "A1",
                "xp_points": 0
            }
        }