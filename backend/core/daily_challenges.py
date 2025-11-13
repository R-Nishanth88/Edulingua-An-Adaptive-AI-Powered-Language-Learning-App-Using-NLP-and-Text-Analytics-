"""
Daily Challenges Module
Auto-generates random writing prompts for daily practice.
"""
from typing import Dict, List, Optional
from datetime import datetime, date
from core.ai_service import generate_ai_response, is_ai_available

# Challenge categories
CHALLENGE_CATEGORIES = {
    "creative": {
        "name": "Creative Writing",
        "prompts": [
            "Write a short story about a day in the life of a time traveler.",
            "Describe your ideal vacation destination in detail.",
            "Write a letter to your future self.",
            "Create a story that begins with 'It was a dark and stormy night...'"
        ]
    },
    "descriptive": {
        "name": "Descriptive Writing",
        "prompts": [
            "Describe your favorite place using all five senses.",
            "Write a detailed description of a memorable meal.",
            "Describe a person who has influenced your life.",
            "Write about a place you've never been but would like to visit."
        ]
    },
    "persuasive": {
        "name": "Persuasive Writing",
        "prompts": [
            "Write a persuasive essay about why reading is important.",
            "Convince someone to try a new hobby or activity.",
            "Argue for or against social media use.",
            "Persuade someone to visit your hometown."
        ]
    },
    "narrative": {
        "name": "Narrative Writing",
        "prompts": [
            "Write about a time you overcame a challenge.",
            "Tell a story about a memorable journey.",
            "Describe an important moment in your life.",
            "Write about a time you learned something important."
        ]
    },
    "academic": {
        "name": "Academic Writing",
        "prompts": [
            "Explain the importance of education in modern society.",
            "Discuss the impact of technology on daily life.",
            "Analyze the benefits of learning a second language.",
            "Explain how to maintain a healthy lifestyle."
        ]
    }
}

def generate_daily_challenge(user_id: Optional[str] = None, category: Optional[str] = None, use_ai: bool = True) -> Dict:
    """
    Generate a daily writing challenge.
    
    Args:
        user_id: Optional user ID for personalized challenges
        category: Optional category (creative, descriptive, persuasive, narrative, academic)
        use_ai: Whether to use AI for challenge generation
    
    Returns:
        Dictionary with challenge prompt and details
    """
    # Select category
    if not category or category not in CHALLENGE_CATEGORIES:
        import random
        category = random.choice(list(CHALLENGE_CATEGORIES.keys()))
    
    category_info = CHALLENGE_CATEGORIES[category]
    
    # Use AI to generate a unique challenge if available
    if use_ai and is_ai_available():
        try:
            prompt = f"""Generate a unique, engaging writing prompt for {category_info['name']} practice.

Category: {category_info['name']}
Style: {category}

Create a prompt that:
- Is clear and specific
- Encourages creative thinking
- Is appropriate for English learners
- Can be completed in 10-15 minutes

Prompt:"""
            
            ai_prompt = generate_ai_response(
                prompt,
                "You are a creative writing teacher generating engaging prompts for language learners.",
                max_tokens=100,
                temperature=0.8
            )
            
            if ai_prompt and len(ai_prompt.strip()) > 20:
                challenge_prompt = ai_prompt.strip()
                method = "ai_generated"
            else:
                # Fallback to predefined prompts
                import random
                challenge_prompt = random.choice(category_info["prompts"])
                method = "predefined"
        except Exception as e:
            print(f"⚠️ AI challenge generation failed: {e}")
            import random
            challenge_prompt = random.choice(category_info["prompts"])
            method = "predefined"
    else:
        # Use predefined prompts
        import random
        challenge_prompt = random.choice(category_info["prompts"])
        method = "predefined"
    
    today = date.today()
    
    return {
        "challenge_id": f"challenge_{today.strftime('%Y%m%d')}_{category}",
        "date": today.isoformat(),
        "category": category,
        "category_name": category_info["name"],
        "prompt": challenge_prompt,
        "word_count_target": 150,  # Target word count
        "time_limit_minutes": 15,  # Suggested time limit
        "difficulty": "medium",
        "method": method,
        "tips": get_challenge_tips(category)
    }

def get_challenge_tips(category: str) -> List[str]:
    """Get tips for completing a challenge in a specific category."""
    tips_by_category = {
        "creative": [
            "Use vivid descriptions and sensory details",
            "Show, don't tell - use actions and dialogue",
            "Let your imagination run wild!"
        ],
        "descriptive": [
            "Use all five senses in your description",
            "Include specific details and examples",
            "Use adjectives and adverbs to paint a picture"
        ],
        "persuasive": [
            "Start with a strong opening statement",
            "Provide clear reasons and examples",
            "End with a compelling conclusion"
        ],
        "narrative": [
            "Use chronological order",
            "Include dialogue and action",
            "Show the significance of the event"
        ],
        "academic": [
            "Use formal language",
            "Structure your essay clearly",
            "Support your points with examples"
        ]
    }
    
    return tips_by_category.get(category, [
        "Write clearly and concisely",
        "Check your grammar and spelling",
        "Review and revise your work"
    ])

def get_challenge_categories() -> List[Dict]:
    """Get all available challenge categories."""
    return [
        {
            "key": key,
            "name": info["name"],
            "description": f"Practice {info['name'].lower()} writing skills"
        }
        for key, info in CHALLENGE_CATEGORIES.items()
    ]

