"""
Interactive Grammar Drills Module
Generates personalized exercises from user mistakes.
"""
from typing import Dict, List, Optional
from core.ai_service import generate_ai_response, is_ai_available
from core.grammar_topic_linking import get_grammar_topic_for_error, GRAMMAR_TOPICS

def generate_grammar_drill(error_type: str, difficulty: str = "medium", use_ai: bool = True) -> Dict:
    """
    Generate a grammar exercise based on a specific error type.
    
    Args:
        error_type: Type of grammar error to practice
        difficulty: Difficulty level (easy, medium, hard)
        use_ai: Whether to use AI for exercise generation
    
    Returns:
        Dictionary with exercise questions and answers
    """
    topic = get_grammar_topic_for_error(error_type)
    
    if not topic:
        return {
            "error": f"No exercise available for error type: {error_type}",
            "questions": []
        }
    
    # Generate exercise using AI
    if use_ai and is_ai_available():
        try:
            prompt = f"""Create a grammar exercise for practicing: {topic['name']}

Error type: {error_type}
Difficulty: {difficulty}

Generate 3 multiple-choice questions with:
1. A sentence with a blank or error
2. 4 answer options (one correct, three incorrect)
3. Clear explanation for the correct answer

Format:
Question 1: [sentence with blank]
A) [option 1]
B) [option 2]
C) [option 3]
D) [option 4]
Correct: [letter]
Explanation: [why this is correct]

Generate 3 questions:"""
            
            ai_exercise = generate_ai_response(
                prompt,
                "You are a grammar teacher creating effective practice exercises.",
                max_tokens=500,
                temperature=0.7
            )
            
            if ai_exercise:
                # Parse AI response into structured format
                questions = parse_ai_exercise(ai_exercise)
                if questions:
                    return {
                        "topic": topic["name"],
                        "error_type": error_type,
                        "difficulty": difficulty,
                        "questions": questions,
                        "total_questions": len(questions),
                        "method": "ai_generated"
                    }
        except Exception as e:
            print(f"⚠️ AI exercise generation failed: {e}")
    
    # Fallback: generate rule-based exercises
    questions = generate_rule_based_exercises(topic, error_type, difficulty)
    
    return {
        "topic": topic["name"],
        "error_type": error_type,
        "difficulty": difficulty,
        "questions": questions,
        "total_questions": len(questions),
        "method": "rule_based"
    }

def parse_ai_exercise(exercise_text: str) -> List[Dict]:
    """Parse AI-generated exercise text into structured format."""
    questions = []
    lines = exercise_text.split('\n')
    
    current_question = None
    current_options = []
    current_correct = None
    current_explanation = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.lower().startswith('question') or (line[0].isdigit() and '.' in line):
            # Save previous question
            if current_question and current_options and current_correct:
                questions.append({
                    "question": current_question,
                    "options": current_options,
                    "correct": current_correct,
                    "explanation": current_explanation or "The correct answer follows the grammar rule."
                })
            
            # Start new question
            current_question = line.split(':', 1)[-1].strip() if ':' in line else line
            current_options = []
            current_correct = None
            current_explanation = None
        
        elif line[0].isupper() and ')' in line:
            # Option (A), B), C), D))
            option_text = line.split(')', 1)[-1].strip()
            current_options.append(option_text)
        
        elif line.lower().startswith('correct:'):
            current_correct = line.split(':', 1)[-1].strip().upper()
        
        elif line.lower().startswith('explanation:'):
            current_explanation = line.split(':', 1)[-1].strip()
    
    # Save last question
    if current_question and current_options and current_correct:
        questions.append({
            "question": current_question,
            "options": current_options,
            "correct": current_correct,
            "explanation": current_explanation or "The correct answer follows the grammar rule."
        })
    
    return questions

def generate_rule_based_exercises(topic: Dict, error_type: str, difficulty: str) -> List[Dict]:
    """Generate exercises using rule-based templates."""
    questions = []
    
    # Template exercises based on topic
    if topic["name"] == "Articles (a, an, the)":
        questions = [
            {
                "question": "I need _____ pen to write.",
                "options": ["a", "an", "the", "no article"],
                "correct": "A",
                "explanation": "Use 'a' before words starting with consonant sounds like 'pen'."
            },
            {
                "question": "She is _____ engineer.",
                "options": ["a", "an", "the", "no article"],
                "correct": "B",
                "explanation": "Use 'an' before words starting with vowel sounds like 'engineer'."
            },
            {
                "question": "I love _____ music.",
                "options": ["a", "an", "the", "no article"],
                "correct": "D",
                "explanation": "No article needed for general concepts like 'music'."
            }
        ]
    
    elif topic["name"] == "Verb Tenses":
        questions = [
            {
                "question": "I _____ to school every day.",
                "options": ["go", "went", "will go", "going"],
                "correct": "A",
                "explanation": "Use present tense 'go' for habitual actions."
            },
            {
                "question": "I _____ to school yesterday.",
                "options": ["go", "went", "will go", "going"],
                "correct": "B",
                "explanation": "Use past tense 'went' for completed actions in the past."
            },
            {
                "question": "I _____ to school tomorrow.",
                "options": ["go", "went", "will go", "going"],
                "correct": "C",
                "explanation": "Use future tense 'will go' for future actions."
            }
        ]
    
    elif topic["name"] == "Prepositions":
        questions = [
            {
                "question": "I live _____ New York.",
                "options": ["in", "on", "at", "by"],
                "correct": "A",
                "explanation": "Use 'in' for cities and countries."
            },
            {
                "question": "The book is _____ the table.",
                "options": ["in", "on", "at", "by"],
                "correct": "B",
                "explanation": "Use 'on' for surfaces like tables."
            },
            {
                "question": "I'll meet you _____ 5 PM.",
                "options": ["in", "on", "at", "by"],
                "correct": "C",
                "explanation": "Use 'at' for specific times."
            }
        ]
    
    else:
        # Generic exercise
        questions = [
            {
                "question": f"Practice: {topic['name']}",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct": "A",
                "explanation": topic.get("rules", [""])[0] if topic.get("rules") else "Follow the grammar rules."
            }
        ]
    
    return questions[:3]  # Limit to 3 questions

def generate_drill_from_mistakes(errors: List[Dict], use_ai: bool = True) -> Dict:
    """
    Generate a personalized drill based on user's mistakes.
    
    Args:
        errors: List of grammar errors from user's text
        use_ai: Whether to use AI for exercise generation
    
    Returns:
        Dictionary with personalized exercises
    """
    if not errors:
        return {
            "message": "No errors found! Great job!",
            "exercises": []
        }
    
    # Count error types
    error_counts = {}
    for error in errors:
        error_type = error.get("type", "general")
        error_counts[error_type] = error_counts.get(error_type, 0) + 1
    
    # Get most common error
    most_common_error = max(error_counts.items(), key=lambda x: x[1]) if error_counts else None
    
    if not most_common_error:
        return {
            "message": "Unable to generate exercises from these errors.",
            "exercises": []
        }
    
    error_type, count = most_common_error
    
    # Determine difficulty based on error frequency
    difficulty = "easy" if count == 1 else "medium" if count <= 3 else "hard"
    
    # Generate drill
    drill = generate_grammar_drill(error_type, difficulty, use_ai=use_ai)
    
    return {
        "message": f"Practice exercise for your most common mistake: {error_type}",
        "error_type": error_type,
        "error_count": count,
        "difficulty": difficulty,
        "exercises": drill.get("questions", []),
        "topic": drill.get("topic", "Grammar")
    }

