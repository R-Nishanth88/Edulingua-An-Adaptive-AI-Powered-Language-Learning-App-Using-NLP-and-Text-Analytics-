from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import settings

# Global MongoDB client
client: AsyncIOMotorClient = None

async def init_db():
    """Initialize MongoDB connection and Beanie ODM"""
    global client
    
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    
    # Import all document models
    from models.user_model import User
    from models.progress_model import Progress
    from models.feedback_model import FeedbackLog
    from models.xp_model import XPBadge
    from models.recommendation_model import Recommendation
    from models.grammar_log_model import GrammarLog
    
    # Initialize Beanie with the document models
    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[
            User,
            Progress,
            FeedbackLog,
            XPBadge,
            Recommendation,
            GrammarLog
        ]
    )
    
    return client

async def close_db():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()

def get_db():
    """Dependency for getting database client"""
    return client