from beanie import Document
from beanie import PydanticObjectId
from datetime import datetime
from pydantic import Field

class XPBadge(Document):
    user_id: PydanticObjectId
    badge_name: str
    earned_on: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "xp_badges"
        indexes = [
            "user_id",
            "badge_name",
        ]