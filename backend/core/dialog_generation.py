"""
Dialog Generation Module - AI-generated conversational practice.
Generates realistic conversation scenarios for language learning.
"""
from typing import List, Dict, Optional
import random

# Try to import transformers for dialog generation
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    pipeline = None

# Global dialog generator
dialog_generator = None

def load_dialog_model():
    """Lazy load dialog generation model."""
    global dialog_generator
    
    if not TRANSFORMERS_AVAILABLE:
        return False
    
    if dialog_generator is not None:
        return True
    
    try:
        # Use GPT-2 or DialoGPT for conversation generation
        dialog_generator = pipeline(
            "text-generation",
            model="microsoft/DialoGPT-medium",
            device=-1  # CPU
        )
        print("✅ Dialog generation model loaded")
        return True
    except Exception as e:
        print(f"⚠️ Could not load dialog model: {e}")
        try:
            # Fallback to GPT-2
            dialog_generator = pipeline(
                "text-generation",
                model="gpt2",
                device=-1
            )
            print("✅ Dialog generation model loaded (GPT-2 fallback)")
            return True
        except Exception as e2:
            print(f"⚠️ Could not load dialog model (fallback): {e2}")
            return False

def generate_dialog(topic: str, level: str = "B1", num_exchanges: int = 5) -> Dict:
    """
    Generate a conversational dialog for practice.
    
    Args:
        topic: Conversation topic (e.g., "introductions", "ordering food", "job interview")
        level: CEFR level (A1, A2, B1, B2, C1, C2)
        num_exchanges: Number of conversation exchanges
    
    Returns:
        Dictionary with dialog structure, prompts, and responses
    """
    if not topic:
        topic = "general conversation"
    
    # Predefined dialog templates based on topic and level
    dialogs = get_dialog_templates(topic, level)
    
    if dialogs:
        selected_dialog = random.choice(dialogs)
        return {
            "topic": topic,
            "level": level,
            "exchanges": selected_dialog["exchanges"][:num_exchanges],
            "scenario": selected_dialog["scenario"],
            "learning_objectives": selected_dialog.get("learning_objectives", []),
            "vocabulary": selected_dialog.get("vocabulary", [])
        }
    
    # Fallback: Generate using model if available
    if TRANSFORMERS_AVAILABLE and load_dialog_model():
        try:
            prompt = f"Conversation about {topic} at {level} level:"
            result = dialog_generator(
                prompt,
                max_length=200,
                num_return_sequences=1,
                temperature=0.7
            )
            if result and len(result) > 0:
                generated_text = result[0].get("generated_text", "")
                # Parse into exchanges (simplified)
                exchanges = parse_generated_dialog(generated_text, num_exchanges)
                return {
                    "topic": topic,
                    "level": level,
                    "exchanges": exchanges,
                    "scenario": f"Practice conversation about {topic}",
                    "learning_objectives": [f"Practice {topic} vocabulary"],
                    "vocabulary": []
                }
        except Exception as e:
            print(f"Error generating dialog: {e}")
    
    # Ultimate fallback: Basic template
    return create_basic_dialog(topic, level, num_exchanges)

def get_dialog_templates(topic: str, level: str) -> List[Dict]:
    """Get predefined dialog templates."""
    templates = {
        "introductions": {
            "A1": [
                {
                    "scenario": "Meeting someone new at a party",
                    "exchanges": [
                        {"speaker": "Person A", "text": "Hello! My name is John. What's your name?", "type": "greeting"},
                        {"speaker": "Person B", "text": "Hi John! I'm Sarah. Nice to meet you.", "type": "greeting"},
                        {"speaker": "Person A", "text": "Nice to meet you too, Sarah! Where are you from?", "type": "question"},
                        {"speaker": "Person B", "text": "I'm from London. How about you?", "type": "question"},
                        {"speaker": "Person A", "text": "I'm from New York. It's great to meet you!", "type": "response"}
                    ],
                    "learning_objectives": ["Introduce yourself", "Ask about origin", "Basic greetings"],
                    "vocabulary": ["introduce", "name", "from", "meet", "nice"]
                }
            ],
            "B1": [
                {
                    "scenario": "Professional networking event",
                    "exchanges": [
                        {"speaker": "Person A", "text": "Good evening! I don't believe we've met. I'm Michael, the marketing director.", "type": "greeting"},
                        {"speaker": "Person B", "text": "Pleasure to meet you, Michael. I'm Emma, I work in finance. How long have you been with the company?", "type": "greeting"},
                        {"speaker": "Person A", "text": "About three years now. And yourself?", "type": "response"},
                        {"speaker": "Person B", "text": "Just started last month, actually. I'm still getting to know everyone.", "type": "response"},
                        {"speaker": "Person A", "text": "Well, welcome aboard! If you need anything, feel free to ask.", "type": "closing"}
                    ],
                    "learning_objectives": ["Professional introductions", "Discuss work experience", "Offer assistance"],
                    "vocabulary": ["director", "finance", "company", "welcome", "assistance"]
                }
            ]
        },
        "ordering_food": {
            "A2": [
                {
                    "scenario": "At a restaurant",
                    "exchanges": [
                        {"speaker": "Waiter", "text": "Good evening! Have you decided what you'd like to order?", "type": "question"},
                        {"speaker": "Customer", "text": "Yes, I'll have the pasta, please.", "type": "request"},
                        {"speaker": "Waiter", "text": "Excellent choice. And what would you like to drink?", "type": "question"},
                        {"speaker": "Customer", "text": "A glass of water, please.", "type": "request"},
                        {"speaker": "Waiter", "text": "Perfect! I'll bring that right away.", "type": "confirmation"}
                    ],
                    "learning_objectives": ["Order food", "Make requests politely", "Restaurant vocabulary"],
                    "vocabulary": ["order", "pasta", "drink", "water", "bring"]
                }
            ]
        },
        "job_interview": {
            "B2": [
                {
                    "scenario": "Job interview for a software developer position",
                    "exchanges": [
                        {"speaker": "Interviewer", "text": "Thank you for coming in today. Can you tell me a bit about your background?", "type": "question"},
                        {"speaker": "Candidate", "text": "Of course. I have five years of experience in software development, primarily working with Python and JavaScript.", "type": "response"},
                        {"speaker": "Interviewer", "text": "That's impressive. What attracted you to this position?", "type": "question"},
                        {"speaker": "Candidate", "text": "I'm particularly interested in the company's focus on AI and machine learning. It aligns with my career goals.", "type": "response"},
                        {"speaker": "Interviewer", "text": "Great! Do you have any questions for us?", "type": "question"},
                        {"speaker": "Candidate", "text": "Yes, I'd like to know about the team structure and growth opportunities.", "type": "question"}
                    ],
                    "learning_objectives": ["Describe experience", "Express interest", "Ask questions"],
                    "vocabulary": ["experience", "background", "attracted", "aligns", "opportunities"]
                }
            ]
        }
    }
    
    topic_lower = topic.lower()
    for key, levels in templates.items():
        if key in topic_lower or topic_lower in key:
            if level in levels:
                return levels[level]
            # Return closest level
            level_order = ["A1", "A2", "B1", "B2", "C1", "C2"]
            for lvl in level_order:
                if lvl in levels:
                    return levels[lvl]
    
    return []

def parse_generated_dialog(text: str, num_exchanges: int) -> List[Dict]:
    """Parse generated text into dialog exchanges."""
    exchanges = []
    lines = text.split('\n')
    
    for line in lines[:num_exchanges * 2]:
        line = line.strip()
        if line and len(line) > 10:
            # Simple parsing - assume alternating speakers
            speaker = "Person A" if len(exchanges) % 2 == 0 else "Person B"
            exchanges.append({
                "speaker": speaker,
                "text": line,
                "type": "response"
            })
    
    return exchanges[:num_exchanges]

def create_basic_dialog(topic: str, level: str, num_exchanges: int) -> Dict:
    """Create a basic dialog template."""
    exchanges = []
    for i in range(num_exchanges):
        speaker = "Person A" if i % 2 == 0 else "Person B"
        exchanges.append({
            "speaker": speaker,
            "text": f"[Practice conversation about {topic}]",
            "type": "practice"
        })
    
    return {
        "topic": topic,
        "level": level,
        "exchanges": exchanges,
        "scenario": f"Practice conversation about {topic}",
        "learning_objectives": [f"Practice {topic} vocabulary"],
        "vocabulary": []
    }

def generate_response(user_input: str, context: List[Dict], topic: str) -> Dict:
    """
    Generate an intelligent, context-aware AI response to user input.
    Uses AI enhancement when available.
    
    Args:
        user_input: User's message
        context: Previous conversation exchanges
        topic: Conversation topic
    
    Returns:
        Dictionary with response and metadata
    """
    # Try AI enhancement first
    try:
        from core.ai_service import enhance_dialog_response, is_ai_available
        if is_ai_available():
            ai_response = enhance_dialog_response(user_input, topic, context)
            if ai_response:
                return {
                    "response": ai_response,
                    "type": "ai_enhanced",
                    "confidence": 0.9
                }
    except Exception as e:
        print(f"⚠️ AI enhancement failed, using rule-based: {e}")
    
    # Fallback to rule-based responses
    user_lower = user_input.lower().strip()
    
    # Get topic-specific responses
    topic_responses = get_topic_responses(topic, user_lower, context)
    if topic_responses:
        return topic_responses
    
    # Greeting responses
    if any(word in user_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
        return {
            "response": "Hello! Nice to meet you. How are you today?",
            "type": "greeting",
            "confidence": 0.9
        }
    
    # Question responses - more specific
    if "?" in user_input or any(word in user_lower for word in ["who", "what", "where", "when", "why", "how"]):
        # Identity questions
        if "who" in user_lower and ("are" in user_lower or "is" in user_lower):
            if "you" in user_lower:
                return {
                    "response": "I'm Alex, your English conversation partner! I'm here to help you practice English. What's your name?",
                    "type": "question_response",
                    "confidence": 0.95
                }
            else:
                return {
                    "response": "That's a good question! Could you tell me more about who you're asking about?",
                    "type": "question_response",
                    "confidence": 0.8
                }
        # Name questions
        elif "what" in user_lower and "name" in user_lower:
            return {
                "response": "My name is Alex. What's your name?",
                "type": "question_response",
                "confidence": 0.9
            }
        # How are you
        elif "how" in user_lower and "are" in user_lower and "you" in user_lower:
            return {
                "response": "I'm doing great, thank you for asking! How about you?",
                "type": "question_response",
                "confidence": 0.9
            }
        # Where questions
        elif "where" in user_lower:
            if "from" in user_lower:
                return {
                    "response": "I'm from the digital world! Where are you from?",
                    "type": "question_response",
                    "confidence": 0.9
                }
            else:
                return {
                    "response": "That's an interesting question! Could you tell me more about what you're asking?",
                    "type": "question_response",
                    "confidence": 0.8
                }
        # When questions
        elif "when" in user_lower:
            return {
                "response": "That's a good question about time! Could you provide a bit more context?",
                "type": "question_response",
                "confidence": 0.8
            }
        # Why questions
        elif "why" in user_lower:
            return {
                "response": "That's an interesting 'why' question! I'd love to help explain. Could you give me more details?",
                "type": "question_response",
                "confidence": 0.8
            }
        # How questions (other than how are you)
        elif "how" in user_lower:
            return {
                "response": "That's a great 'how' question! Let me think about the best way to explain this...",
                "type": "question_response",
                "confidence": 0.8
            }
        # Other questions
        else:
            return {
                "response": "That's a good question! Could you provide a bit more context so I can give you a better answer?",
                "type": "question_response",
                "confidence": 0.7
            }
    
    # Agreement responses
    if any(word in user_lower for word in ["yes", "yeah", "sure", "okay", "ok", "alright"]):
        return {
            "response": "Perfect! I'm glad we're on the same page. What would you like to talk about next?",
            "type": "agreement",
            "confidence": 0.8
        }
    
    # Disagreement responses
    if any(word in user_lower for word in ["no", "not", "don't", "can't", "won't"]):
        return {
            "response": "I understand. That's okay! Is there something else you'd like to discuss?",
            "type": "disagreement",
            "confidence": 0.8
        }
    
    # Thank you responses
    if any(word in user_lower for word in ["thank", "thanks", "appreciate"]):
        return {
            "response": "You're very welcome! I'm happy to help. Is there anything else you'd like to know?",
            "type": "gratitude",
            "confidence": 0.9
        }
    
    # Name responses
    if "name" in user_lower and ("my" in user_lower or "i'm" in user_lower or "i am" in user_lower):
        # Try to extract name
        import re
        name_match = re.search(r'(?:my name is|i\'?m|i am)\s+([A-Z][a-z]+)', user_input, re.IGNORECASE)
        if name_match:
            name = name_match.group(1)
            return {
                "response": f"Nice to meet you, {name}! It's a pleasure talking with you. How can I help you today?",
                "type": "introduction",
                "confidence": 0.9
            }
        else:
            return {
                "response": "Nice to meet you! What's your name?",
                "type": "introduction",
                "confidence": 0.8
            }
    
    # Context-aware responses based on previous exchanges
    if context and len(context) > 0:
        last_exchange = context[-1] if isinstance(context[-1], dict) else {}
        last_text = last_exchange.get("text", "").lower() if isinstance(last_exchange, dict) else ""
        
        # If last was a question, provide a relevant response
        if "?" in last_text:
            if "how are you" in last_text:
                return {
                    "response": "I'm doing well, thank you! How about you?",
                    "type": "response",
                    "confidence": 0.8
                }
            elif "what" in last_text and "name" in last_text:
                return {
                    "response": "My name is Alex. What's yours?",
                    "type": "response",
                    "confidence": 0.8
                }
    
    # Topic-specific responses
    if topic == "introductions":
        if "from" in user_lower:
            return {
                "response": "That's interesting! I'd love to hear more about your hometown. What do you like most about it?",
                "type": "topic_response",
                "confidence": 0.8
            }
        elif "work" in user_lower or "job" in user_lower:
            return {
                "response": "That sounds like an interesting job! What do you enjoy most about your work?",
                "type": "topic_response",
                "confidence": 0.8
            }
    
    elif topic == "ordering_food":
        if any(word in user_lower for word in ["menu", "order", "food", "eat"]):
            return {
                "response": "Great choice! Would you like anything to drink with that?",
                "type": "topic_response",
                "confidence": 0.8
            }
    
    elif topic == "job_interview":
        if any(word in user_lower for word in ["experience", "worked", "job", "position"]):
            return {
                "response": "That's impressive experience! What skills do you think are most important for this role?",
                "type": "topic_response",
                "confidence": 0.8
            }
    
    # Default intelligent response
    return {
        "response": "I see. That's interesting! Can you tell me more about that?",
        "type": "general",
        "confidence": 0.6
    }

def get_topic_responses(topic: str, user_input: str, context: List[Dict]) -> Optional[Dict]:
    """Get topic-specific intelligent responses."""
    topic_lower = topic.lower()
    user_lower = user_input.lower()
    
    # Introductions topic
    if "introduction" in topic_lower:
        if "nice to meet" in user_lower or "pleasure" in user_lower:
            return {
                "response": "The pleasure is all mine! I'm excited to get to know you better.",
                "type": "greeting",
                "confidence": 0.9
            }
        elif "where" in user_lower and "from" in user_lower:
            return {
                "response": "I'm from the digital world! Where are you from?",
                "type": "question_response",
                "confidence": 0.8
            }
    
    # Ordering food topic
    elif "order" in topic_lower or "food" in topic_lower:
        if any(word in user_lower for word in ["pasta", "pizza", "burger", "salad"]):
            return {
                "response": "Excellent choice! That's one of our most popular items. Would you like anything to drink?",
                "type": "topic_response",
                "confidence": 0.9
            }
        elif "drink" in user_lower or "water" in user_lower or "coffee" in user_lower:
            return {
                "response": "Perfect! I'll bring that right away. Is there anything else I can get for you?",
                "type": "topic_response",
                "confidence": 0.9
            }
    
    # Job interview topic
    elif "interview" in topic_lower or "job" in topic_lower:
        if "experience" in user_lower:
            return {
                "response": "That's valuable experience! How do you think your background aligns with this position?",
                "type": "topic_response",
                "confidence": 0.8
            }
        elif "question" in user_lower:
            return {
                "response": "Absolutely! We encourage questions. What would you like to know about the role or company?",
                "type": "topic_response",
                "confidence": 0.9
            }
    
    return None

def evaluate_dialog_response(user_response: str, expected_response: str, context: List[Dict]) -> Dict:
    """
    Evaluate user's dialog response against expected response.
    
    Args:
        user_response: User's actual response
        expected_response: Expected/correct response
        context: Conversation context
    
    Returns:
        Dictionary with evaluation scores and feedback
    """
    from core.semantic_similarity import calculate_semantic_similarity
    from core.grammar_analysis import detect_grammar_errors
    
    # Calculate semantic similarity
    similarity = calculate_semantic_similarity(user_response, expected_response)
    
    # Check grammar
    grammar_errors = detect_grammar_errors(user_response)
    grammar_score = max(0, 1 - (len(grammar_errors) * 0.1))
    
    # Overall score
    overall_score = (similarity * 0.6 + grammar_score * 0.4)
    
    feedback = []
    if similarity < 0.5:
        feedback.append("Try to express the same idea more clearly.")
    if len(grammar_errors) > 0:
        feedback.append(f"Watch out for {len(grammar_errors)} grammar error(s).")
    if overall_score > 0.8:
        feedback.append("Excellent response!")
    
    return {
        "score": round(overall_score * 100, 1),
        "similarity_score": round(similarity * 100, 1),
        "grammar_score": round(grammar_score * 100, 1),
        "grammar_errors": len(grammar_errors),
        "feedback": feedback,
        "suggestions": [expected_response] if similarity < 0.7 else []
    }

