from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analyze, user, chatbot, gamify, recommend, progress, corrector, advanced_features, advanced_ai_features, evaluation, model_evaluation
from models.database import init_db, close_db
from config import settings

app = FastAPI(
    title="EduLingua Pro API",
    description="Adaptive AI Language Learning Platform using NLP and Text Analytics",
    version="1.0.0"
)

# CORS middleware - must be added before routers
# Handle CORS_ORIGINS as string or list
cors_origins = settings.CORS_ORIGINS
if isinstance(cors_origins, str):
    # Split by comma if it's a comma-separated string
    if ',' in cors_origins:
        cors_origins = [origin.strip() for origin in cors_origins.split(',')]
    else:
        cors_origins = [cors_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(analyze.router)
app.include_router(user.router)
app.include_router(chatbot.router)
app.include_router(gamify.router)
app.include_router(recommend.router)
app.include_router(progress.router)
app.include_router(corrector.router)
app.include_router(advanced_features.router)
app.include_router(advanced_ai_features.router)
app.include_router(evaluation.router)
app.include_router(model_evaluation.router)

# Initialize MongoDB connection on startup
@app.on_event("startup")
async def startup_event():
    try:
        await init_db()
        print("✅ MongoDB connected successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not connect to MongoDB: {e}")
        print("The app will continue, but database features may not work until MongoDB is running.")

# Close MongoDB connection on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    await close_db()
    print("MongoDB connection closed")

@app.get("/")
async def root():
    return {
        "message": "Welcome to EduLingua Pro API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
