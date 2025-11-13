from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models.user_model import User
from models.xp_model import XPBadge
from core.auth import get_current_user

router = APIRouter(prefix="/gamify", tags=["gamify"])

class XPUpdate(BaseModel):
    points: int
    reason: str

BADGE_CRITERIA = {
    "Grammar Guru": {"xp_threshold": 100, "description": "Earned 100 XP from grammar improvements"},
    "Lexical Legend": {"xp_threshold": 200, "description": "Earned 200 XP from vocabulary expansion"},
    "Fluency Pro": {"xp_threshold": 500, "description": "Earned 500 XP from consistent practice"},
    "Writing Master": {"xp_threshold": 1000, "description": "Earned 1000 XP from writing practice"},
    "Streak Champion": {"xp_threshold": 50, "description": "Maintained a 7-day practice streak"},
    "CEFR Climber": {"xp_threshold": 300, "description": "Improved your CEFR level"}
}

@router.post("/xp")
async def update_xp(
    xp_data: XPUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update user XP points and check for badge eligibility."""
    if xp_data.points <= 0:
        raise HTTPException(status_code=400, detail="XP points must be positive")
    
    # Update user XP
    current_user.xp_points += xp_data.points
    await current_user.save()
    
    # Check for new badges
    new_badges = []
    user_badges_list = await XPBadge.find(XPBadge.user_id == current_user.id).to_list()
    user_badges = {badge.badge_name for badge in user_badges_list}
    
    for badge_name, criteria in BADGE_CRITERIA.items():
        if badge_name not in user_badges and current_user.xp_points >= criteria["xp_threshold"]:
            # Award badge
            new_badge = XPBadge(
                user_id=current_user.id,
                badge_name=badge_name
            )
            await new_badge.insert()
            new_badges.append({
                "name": badge_name,
                "description": criteria["description"]
            })
    
    return {
        "xp_points": current_user.xp_points,
        "new_badges": new_badges,
        "message": f"Earned {xp_data.points} XP! {xp_data.reason}"
    }

@router.get("/badges")
async def get_badges(
    current_user: User = Depends(get_current_user)
):
    """Get all badges for the current user."""
    badges = await XPBadge.find(XPBadge.user_id == current_user.id).to_list()
    
    return {
        "badges": [
            {
                "name": badge.badge_name,
                "earned_on": badge.earned_on.isoformat() if badge.earned_on else None
            }
            for badge in badges
        ],
        "total_badges": len(badges),
        "available_badges": [
            {
                "name": name,
                "description": criteria["description"],
                "earned": any(b.badge_name == name for b in badges)
            }
            for name, criteria in BADGE_CRITERIA.items()
        ]
    }

@router.get("/leaderboard")
async def get_leaderboard(
    limit: int = 10
):
    """Get leaderboard of top users by XP."""
    top_users = await User.find_all().sort(-User.xp_points).limit(limit).to_list()
    
    return {
        "leaderboard": [
            {
                "username": user.username,
                "xp_points": user.xp_points,
                "cefr_level": user.cefr_level,
                "rank": idx + 1
            }
            for idx, user in enumerate(top_users)
        ]
    }