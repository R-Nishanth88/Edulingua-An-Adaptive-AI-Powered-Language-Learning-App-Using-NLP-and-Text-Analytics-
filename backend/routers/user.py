from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from datetime import timedelta
from models.user_model import User
from core.auth import verify_password, get_password_hash, create_access_token, get_current_user
from config import settings

router = APIRouter(prefix="/user", tags=["user"])

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    username: str
    cefr_level: str
    xp_points: int

@router.post("/signup", response_model=Token)
async def signup(user_data: UserSignup):
    """User registration endpoint."""
    try:
        # Check if user already exists
        existing_email = await User.find_one(User.email == user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        existing_username = await User.find_one(User.username == user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password,
            cefr_level="A1",
            xp_points=0
        )
        
        await new_user.insert()
    except Exception as e:
        # Check if it's a MongoDB connection error
        error_msg = str(e).lower()
        if "connection" in error_msg or "refused" in error_msg or "timeout" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection failed. Please ensure MongoDB is running."
            )
        # Re-raise HTTP exceptions
        if isinstance(e, HTTPException):
            raise
        # For other errors, log and return generic error
        print(f"Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration. Please try again."
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(new_user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(new_user.id),
        "username": new_user.username,
        "cefr_level": new_user.cefr_level,
        "xp_points": new_user.xp_points
    }

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """User login endpoint."""
    try:
        user = await User.find_one(User.email == user_data.email)
        
        if not user or not verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
    except Exception as e:
        error_msg = str(e).lower()
        if "connection" in error_msg or "refused" in error_msg or "timeout" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection failed. Please ensure MongoDB is running."
            )
        if isinstance(e, HTTPException):
            raise
        print(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login. Please try again."
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user.id),
        "username": user.username,
        "cefr_level": user.cefr_level,
        "xp_points": user.xp_points
    }

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "cefr_level": current_user.cefr_level,
        "xp_points": current_user.xp_points,
        "created_at": current_user.created_at
    }
