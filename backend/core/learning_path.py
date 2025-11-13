"""
Predictive Learning Path Generation - Recommends next lessons using user performance analytics.
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from beanie import PydanticObjectId
from collections import Counter

async def generate_learning_path(user_id: PydanticObjectId, days: int = 30) -> Dict:
    """
    Generate personalized learning path based on user performance.
    
    Args:
        user_id: User identifier
        days: Number of days to analyze
    
    Returns:
        Dictionary with recommended learning path
    """
    from models.progress_model import Progress
    from models.grammar_log_model import GrammarLog
    from models.user_model import User
    from core.error_pattern_mining import mine_error_patterns
    
    # Get user
    user = await User.get(user_id)
    current_level = user.cefr_level if user else "B1"
    
    # Get error patterns
    error_analysis = await mine_error_patterns(user_id, days)
    
    # Get recent progress
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    recent_progress = await Progress.find(
        Progress.user_id == user_id,
        Progress.date >= cutoff_date
    ).sort(-Progress.date).limit(10).to_list()
    
    # Determine learning priorities
    priorities = determine_learning_priorities(error_analysis, recent_progress, current_level)
    
    # Generate lesson recommendations
    lessons = generate_lesson_recommendations(priorities, current_level)
    
    # Calculate progress milestones
    milestones = calculate_milestones(current_level, recent_progress)
    
    return {
        "user_id": str(user_id),
        "current_level": current_level,
        "learning_path": {
            "next_lessons": lessons,
            "priorities": priorities,
            "estimated_completion": calculate_estimated_completion(lessons),
            "milestones": milestones
        },
        "performance_insights": {
            "strengths": identify_strengths_from_progress(recent_progress),
            "weaknesses": error_analysis.get("improvement_areas", []),
            "progress_rate": calculate_progress_rate(recent_progress)
        }
    }

def determine_learning_priorities(error_analysis: Dict, progress_list: List, current_level: str) -> List[Dict]:
    """Determine learning priorities based on errors and progress."""
    priorities = []
    
    # Priority 1: Most common errors
    most_common_errors = error_analysis.get("most_common_errors", {})
    for error_type, count in list(most_common_errors.items())[:3]:
        priorities.append({
            "topic": get_topic_for_error(error_type),
            "priority": "high" if count >= 10 else "medium",
            "reason": f"Frequent {error_type} errors ({count} occurrences)",
            "estimated_time": "2-3 hours"
        })
    
    # Priority 2: Level-appropriate topics
    level_topics = get_level_topics(current_level)
    for topic in level_topics[:2]:
        priorities.append({
            "topic": topic,
            "priority": "medium",
            "reason": f"Recommended for {current_level} level",
            "estimated_time": "1-2 hours"
        })
    
    return priorities[:5]  # Top 5 priorities

def get_topic_for_error(error_type: str) -> str:
    """Map error type to learning topic."""
    topic_mapping = {
        "word_order": "Sentence Structure",
        "missing_article": "Articles (a, an, the)",
        "missing_infinitive": "Infinitives and Gerunds",
        "subject_verb_agreement": "Subject-Verb Agreement",
        "spelling": "Spelling and Vocabulary",
        "punctuation": "Punctuation Rules",
        "capitalization": "Capitalization Rules"
    }
    return topic_mapping.get(error_type, "Grammar Fundamentals")

def get_level_topics(level: str) -> List[str]:
    """Get recommended topics for a CEFR level."""
    topics = {
        "A1": ["Basic Greetings", "Numbers and Dates", "Simple Present Tense", "Common Verbs"],
        "A2": ["Past Tense", "Future Tense", "Adjectives", "Prepositions", "Articles"],
        "B1": ["Present Perfect", "Conditionals", "Modal Verbs", "Phrasal Verbs", "Complex Sentences"],
        "B2": ["Passive Voice", "Reported Speech", "Advanced Vocabulary", "Essay Writing", "Formal Language"],
        "C1": ["Advanced Grammar", "Academic Writing", "Idiomatic Expressions", "Nuanced Vocabulary"],
        "C2": ["Mastery Level", "Professional Writing", "Literary Analysis", "Advanced Discourse"]
    }
    return topics.get(level, topics["B1"])

def generate_lesson_recommendations(priorities: List[Dict], current_level: str) -> List[Dict]:
    """Generate specific lesson recommendations."""
    lessons = []
    
    for i, priority in enumerate(priorities[:5]):
        topic = priority["topic"]
        lessons.append({
            "lesson_id": f"lesson_{i+1}",
            "title": f"Master {topic}",
            "topic": topic,
            "level": current_level,
            "priority": priority["priority"],
            "estimated_duration": priority.get("estimated_time", "1-2 hours"),
            "objectives": get_lesson_objectives(topic),
            "exercises": get_lesson_exercises(topic),
            "resources": get_lesson_resources(topic)
        })
    
    return lessons

def get_lesson_objectives(topic: str) -> List[str]:
    """Get learning objectives for a topic."""
    objectives = {
        "Sentence Structure": [
            "Understand Subject-Verb-Object order",
            "Practice constructing grammatically correct sentences",
            "Identify and fix word order errors"
        ],
        "Articles (a, an, the)": [
            "Learn when to use 'a', 'an', and 'the'",
            "Practice article usage in context",
            "Avoid common article mistakes"
        ],
        "Infinitives and Gerunds": [
            "Understand when to use infinitives vs gerunds",
            "Practice with common verbs",
            "Master 'to' + verb constructions"
        ]
    }
    return objectives.get(topic, [f"Master {topic}", f"Practice {topic} in context"])

def get_lesson_exercises(topic: str) -> List[str]:
    """Get exercise types for a topic."""
    exercises = {
        "Sentence Structure": [
            "Rearrange scrambled sentences",
            "Complete sentences with correct structure",
            "Identify and correct word order errors"
        ],
        "Articles (a, an, the)": [
            "Fill in the blanks with articles",
            "Choose correct article",
            "Article usage in paragraphs"
        ]
    }
    return exercises.get(topic, [f"Practice {topic} exercises", f"{topic} quizzes"])

def get_lesson_resources(topic: str) -> List[str]:
    """Get learning resources for a topic."""
    return [
        f"{topic} grammar guide",
        f"{topic} practice worksheets",
        f"{topic} video tutorials"
    ]

def calculate_milestones(current_level: str, progress_list: List) -> List[Dict]:
    """Calculate learning milestones."""
    milestones = []
    
    level_progression = ["A1", "A2", "B1", "B2", "C1", "C2"]
    current_index = level_progression.index(current_level) if current_level in level_progression else 2
    
    # Next level milestone
    if current_index < len(level_progression) - 1:
        next_level = level_progression[current_index + 1]
        milestones.append({
            "milestone": f"Reach {next_level} level",
            "progress": calculate_level_progress(current_level, progress_list),
            "estimated_time": "2-3 months"
        })
    
    # Error reduction milestone
    if progress_list:
        avg_errors = sum(p.grammar_errors for p in progress_list if hasattr(p, 'grammar_errors')) / len(progress_list)
        milestones.append({
            "milestone": f"Reduce average errors to < 2 per text",
            "current_avg": round(avg_errors, 1),
            "target": 2.0,
            "progress": max(0, min(100, (1 - avg_errors / 10) * 100))
        })
    
    return milestones

def calculate_level_progress(current_level: str, progress_list: List) -> float:
    """Calculate progress toward next level."""
    if not progress_list:
        return 0.0
    
    # Simplified: based on error reduction and consistency
    recent_errors = [p.grammar_errors for p in progress_list[-5:] if hasattr(p, 'grammar_errors')]
    if not recent_errors:
        return 50.0
    
    avg_errors = sum(recent_errors) / len(recent_errors)
    # Lower errors = higher progress
    progress = max(0, min(100, (1 - avg_errors / 10) * 100))
    return round(progress, 1)

def calculate_estimated_completion(lessons: List[Dict]) -> str:
    """Calculate estimated time to complete lessons."""
    total_hours = 0
    for lesson in lessons:
        duration = lesson.get("estimated_duration", "1-2 hours")
        # Extract number (simplified)
        if "1-2" in duration:
            total_hours += 1.5
        elif "2-3" in duration:
            total_hours += 2.5
        else:
            total_hours += 1.0
    
    weeks = total_hours / 5  # Assuming 5 hours per week
    if weeks < 1:
        return f"{int(weeks * 7)} days"
    elif weeks < 4:
        return f"{int(weeks)} weeks"
    else:
        return f"{int(weeks / 4)} months"

def identify_strengths_from_progress(progress_list: List) -> List[str]:
    """Identify strengths from progress data."""
    if not progress_list:
        return []
    
    strengths = []
    
    # Check readability trend
    readability_scores = [p.readability for p in progress_list if hasattr(p, 'readability')]
    if readability_scores and readability_scores[-1] > 60:
        strengths.append("Good readability")
    
    # Check error reduction
    error_counts = [p.grammar_errors for p in progress_list if hasattr(p, 'grammar_errors')]
    if len(error_counts) >= 2 and error_counts[-1] < error_counts[0]:
        strengths.append("Improving grammar accuracy")
    
    return strengths

def calculate_progress_rate(progress_list: List) -> float:
    """Calculate overall progress rate (0-100)."""
    if len(progress_list) < 2:
        return 50.0
    
    # Calculate improvement in errors
    first_errors = progress_list[0].grammar_errors if hasattr(progress_list[0], 'grammar_errors') else 5
    last_errors = progress_list[-1].grammar_errors if hasattr(progress_list[-1], 'grammar_errors') else 5
    
    if first_errors == 0:
        improvement = 0
    else:
        improvement = ((first_errors - last_errors) / first_errors) * 100
    
    return round(max(0, min(100, 50 + improvement)), 1)

