"""
Intelligent Chatbot Module - Context-aware conversational AI tutor.
Provides natural, helpful responses based on user queries and context.
"""
from typing import List, Dict, Optional
import re
from core.grammar_analysis import detect_grammar_errors, correct_grammar
from core.lexical_semantic import suggest_synonyms, extract_keywords

# Optional imports
try:
    from core.readability import calculate_readability
except ImportError:
    calculate_readability = None

try:
    from core.tone_style import analyze_tone_and_style
    analyze_tone_style = analyze_tone_and_style
except ImportError:
    try:
        from core.tone_style import analyze_tone
        analyze_tone_style = analyze_tone
    except ImportError:
        analyze_tone_style = None

# Enhanced knowledge base with more topics
KNOWLEDGE_BASE = {
    "grammar": {
        "articles": {
            "keywords": ["article", "a", "an", "the", "indefinite", "definite"],
            "explanation": """Articles are words that define a noun as specific or unspecific.

**Indefinite Articles (a/an):**
- Use 'a' before words starting with a consonant sound: "a book", "a university"
- Use 'an' before words starting with a vowel sound: "an apple", "an hour"

**Definite Article (the):**
- Use 'the' when referring to something specific: "the book I read"
- Use 'the' with unique things: "the sun", "the moon"
- Don't use 'the' with general concepts: "I love music" (not "the music")

**Examples:**
- "I need a pen" (any pen)
- "I need the pen" (specific pen)
- "She is an engineer" (profession)
- "The engineer fixed the problem" (specific engineer)""",
            "examples": [
                "I saw a cat in the garden.",
                "An hour passed quickly.",
                "The cat I saw was black."
            ]
        },
        "tenses": {
            "keywords": ["tense", "past", "present", "future", "verb", "time"],
            "explanation": """Verb tenses indicate when an action occurs.

**Present Tense:**
- Simple Present: "I study English every day."
- Present Continuous: "I am studying right now."
- Present Perfect: "I have studied for three years."

**Past Tense:**
- Simple Past: "I studied yesterday."
- Past Continuous: "I was studying when you called."
- Past Perfect: "I had studied before the test."

**Future Tense:**
- Simple Future: "I will study tomorrow."
- Future Continuous: "I will be studying at 3 PM."
- Future Perfect: "I will have studied by then."

**Key Tip:** Match the tense to the time of the action!""",
            "examples": [
                "I go to school every day. (Present)",
                "I went to school yesterday. (Past)",
                "I will go to school tomorrow. (Future)"
            ]
        },
        "prepositions": {
            "keywords": ["preposition", "in", "on", "at", "by", "with", "for"],
            "explanation": """Prepositions show relationships between words.

**Time Prepositions:**
- "in" for months/years: "in January", "in 2024"
- "on" for days: "on Monday", "on my birthday"
- "at" for specific times: "at 3 PM", "at night"

**Place Prepositions:**
- "in" for enclosed spaces: "in the room", "in the box"
- "on" for surfaces: "on the table", "on the wall"
- "at" for specific points: "at the door", "at the station"

**Common Mistakes:**
- ❌ "I am in home" → ✅ "I am at home"
- ❌ "I study in Monday" → ✅ "I study on Monday" """,
            "examples": [
                "I live in New York.",
                "The book is on the table.",
                "I'll meet you at 5 PM."
            ]
        },
        "sentence_structure": {
            "keywords": ["sentence", "structure", "order", "word order", "syntax"],
            "explanation": """English follows a Subject-Verb-Object (SVO) order.

**Basic Structure:**
Subject + Verb + Object
"I + eat + apples."

**Common Mistakes:**
- ❌ "I name Nishanth" → ✅ "My name is Nishanth"
- ❌ "I am student" → ✅ "I am a student"
- ❌ "She goes to school every day" (correct!)

**Questions:**
- Invert subject and verb: "Are you ready?" (not "You are ready?")
- Use question words: "What is your name?"

**Tips:**
- Always include a subject (except in commands)
- Match subject and verb: "He goes" not "He go"
- Put adjectives before nouns: "a big house" """,
            "examples": [
                "My name is John. (Subject + Verb + Complement)",
                "I study English. (Subject + Verb + Object)",
                "What is your name? (Question form)"
            ]
        }
    },
    "vocabulary": {
        "synonyms": {
            "keywords": ["synonym", "similar", "same meaning", "alternative"],
            "explanation": "Synonyms are words with similar meanings. For example, 'happy' and 'joyful' are synonyms. Would you like to know synonyms for a specific word?",
        },
        "word_meaning": {
            "keywords": ["meaning", "definition", "what does", "explain"],
            "explanation": "I can explain word meanings! Just tell me which word you'd like to learn about, and I'll provide a clear definition with examples.",
        }
    },
    "writing": {
        "tips": {
            "keywords": ["writing", "improve", "better", "tips", "advice"],
            "explanation": """Here are some writing tips:

1. **Be Clear:** Use simple, direct language
2. **Be Concise:** Remove unnecessary words
3. **Use Active Voice:** "I wrote the letter" (not "The letter was written by me")
4. **Vary Sentence Length:** Mix short and long sentences
5. **Proofread:** Always check for errors

Would you like tips on a specific writing topic?""",
        }
    }
}

def analyze_query_intent(query: str) -> Dict:
    """Analyze user query to understand intent and extract information."""
    query_lower = query.lower().strip()
    
    intent = {
        "type": "general",
        "confidence": 0.5,
        "topic": None,
        "subtopic": None,
        "is_question": "?" in query,
        "is_greeting": any(word in query_lower for word in ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]),
        "is_farewell": any(word in query_lower for word in ["bye", "goodbye", "see you", "thanks", "thank you"]),
        "needs_correction": False,
        "keywords": []
    }
    
    # Check for grammar correction request
    if any(word in query_lower for word in ["correct", "fix", "wrong", "error", "mistake", "check"]):
        intent["type"] = "correction"
        intent["confidence"] = 0.8
        intent["needs_correction"] = True
    
    # Also detect malformed sentences even without correction keywords
    if not intent["needs_correction"]:
        malformed_patterns = [
            r'^(i|she|he|they|we|you)\s+\w+\s+name',  # "i nishanth name"
            r'^\w+\s+am\s+i$',  # "nishanth am i"
            r'^name\s+\w+',  # "name nishanth"
            r'^\w+\s+name$',  # "nishanth name"
            r'^i\s+am\s+\w+$',  # "i am student" (might need article)
            r'^i\s+like\s+\w+\s+\w+$',  # "i like play football" (missing to)
        ]
        for pattern in malformed_patterns:
            if re.match(pattern, query, re.IGNORECASE):
                intent["type"] = "correction"
                intent["confidence"] = 0.7
                intent["needs_correction"] = True
                break
    
    # Handle identity questions first (before grammar matching)
    if any(phrase in query_lower for phrase in ["who are you", "what are you", "who is this", "what is this"]):
        intent["type"] = "identity"
        intent["confidence"] = 0.95
        return intent
    
    # Check for grammar questions (but not if it's an identity question)
    for category, topics in KNOWLEDGE_BASE.items():
        for topic_key, topic_info in topics.items():
            if any(keyword in query_lower for keyword in topic_info.get("keywords", [])):
                # Don't match if it's clearly an identity question
                if not any(phrase in query_lower for phrase in ["who are", "what are", "who is", "what is"]):
                    intent["type"] = category
                    intent["topic"] = category
                    intent["subtopic"] = topic_key
                    intent["confidence"] = 0.9
                    break
    
    # Extract keywords
    words = query_lower.split()
    intent["keywords"] = [w for w in words if len(w) > 3]
    
    return intent

def generate_intelligent_response(query: str, context: Optional[List[Dict]] = None) -> Dict:
    """
    Generate an intelligent, context-aware response.
    Uses AI enhancement when available.
    
    Args:
        query: User's query
        context: Previous conversation context
    
    Returns:
        Dictionary with response, suggestions, and metadata
    """
    # Analyze intent first to check if this needs correction
    intent = analyze_query_intent(query)
    
    # If it's a correction request, handle it with rule-based logic first (more reliable)
    # Only use AI for non-correction queries
    if not intent.get("needs_correction", False):
        # Try AI enhancement for non-correction queries (focused on grammar and EduLingua)
        try:
            from core.ai_service import enhance_chatbot_response, is_ai_available
            if is_ai_available():
                ai_response = enhance_chatbot_response(query, context)
                if ai_response:
                    # Filter to ensure response is grammar/EduLingua focused
                    # If AI gives generic response, fall through to rule-based
                    if len(ai_response) > 50 and any(keyword in ai_response.lower() for keyword in [
                        "grammar", "sentence", "correct", "english", "word", "vocabulary", 
                        "writing", "edulingua", "learn", "practice", "rule", "error", "mistake"
                    ]):
                        return {
                            "response": ai_response,
                            "suggestions": ["Check grammar in dashboard", "Learn more grammar rules", "Practice vocabulary"],
                            "type": "ai_enhanced"
                        }
        except Exception as e:
            print(f"⚠️ AI enhancement failed, using rule-based: {e}")
    
    # Continue with rule-based responses (including corrections)
    
    # Handle greetings
    if intent["is_greeting"]:
        return {
            "response": """Hello! 👋 I'm **EduLingua Pro**, your AI English grammar tutor!

I specialize in helping you improve your English through:

📚 **Grammar Correction & Analysis**
   - Fix grammar errors and sentence structure
   - Explain grammar rules with examples
   - Check articles, tenses, prepositions, word order

📖 **Vocabulary & Word Usage**
   - Learn word meanings and synonyms
   - Understand proper word usage in context
   - Build your vocabulary

✍️ **Writing Improvement**
   - Get feedback on your writing style
   - Learn to write clearly and correctly
   - Improve sentence formation

🎯 **EduLingua Features**
   - Use the **Dashboard** to analyze your text
   - Get detailed grammar corrections
   - Track your learning progress

**Try this:** Go to the Dashboard and type a sentence to get instant grammar analysis!

What grammar topic would you like help with today?""",
            "suggestions": [
                "Explain grammar rules",
                "Check my sentence",
                "Help with vocabulary",
                "Use the dashboard"
            ],
            "type": "greeting"
        }
    
    # Handle identity questions
    if intent["type"] == "identity" or any(phrase in query.lower() for phrase in ["who are you", "what are you", "who is this"]):
        return {
            "response": """Hello! I'm **EduLingua Pro**, your AI English grammar tutor! 👋

I'm specialized in helping you learn English grammar and improve your language skills.

**What I Do:**
✅ **Grammar Correction** - Fix errors in your sentences and explain why
✅ **Grammar Rules** - Teach articles, tenses, prepositions, sentence structure
✅ **Vocabulary Help** - Explain word meanings, synonyms, and usage
✅ **Writing Feedback** - Improve your writing style and clarity
✅ **Text Analysis** - Use the Dashboard to analyze your text for grammar, vocabulary, and readability

**EduLingua Features:**
• Dashboard text analysis with detailed feedback
• Grammar error detection and correction
• Rephrasing suggestions
• Progress tracking
• Adaptive learning recommendations

**Best Way to Use Me:**
1. Ask me grammar questions (e.g., "Explain articles")
2. Check sentences (e.g., "Check: I am student")
3. Use the Dashboard to analyze your text
4. Learn vocabulary and word usage

What grammar topic would you like help with?""",
            "suggestions": [
                "Explain grammar rules",
                "Check my sentence",
                "Use the dashboard",
                "Help with vocabulary"
            ],
            "type": "identity"
        }
    
    # Handle farewells
    if intent["is_farewell"]:
        return {
            "response": "You're welcome! Keep practicing your grammar and English skills. Remember to use the Dashboard to analyze your text and track your progress. Feel free to come back anytime if you have grammar questions! Good luck with your English learning! 🎓",
            "suggestions": ["Use the dashboard", "Practice grammar", "Learn more rules"],
            "type": "farewell"
        }
    
    # Handle grammar correction requests
    if intent["needs_correction"]:
        # Try to extract the sentence to correct
        # Look for patterns like "correct: sentence" or "fix: sentence" or just a sentence after correction keywords
        text_to_correct = None
        
        # Pattern 1: "correct this: sentence" or "fix: sentence"
        colon_match = re.search(r'(?:correct|fix|check)\s*(?:this|it)?:?\s*(.+)', query, re.IGNORECASE)
        if colon_match:
            text_to_correct = colon_match.group(1).strip()
        
        # Pattern 2: Sentence after correction keywords
        if not text_to_correct:
            sentences = re.split(r'[.!?]+', query)
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 5:
                    # Remove correction keywords
                    cleaned = re.sub(r'\b(correct|fix|check|wrong|error|mistake)\b', '', sentence, flags=re.IGNORECASE).strip()
                    if len(cleaned) > 3 and cleaned != sentence:
                        text_to_correct = cleaned
                        break
        
        # Pattern 3: If query itself looks like a malformed sentence (common patterns)
        if not text_to_correct:
            # Check for common malformed patterns
            malformed_patterns = [
                r'^(i|she|he|they|we|you)\s+\w+',  # "i nishanth name"
                r'^\w+\s+am\s+i$',  # "nishanth am i"
                r'^name\s+\w+',  # "name nishanth"
                r'^\w+\s+name',  # "nishanth name"
                r'^i\s+am\s+\w+$',  # "i am student" (missing article)
                r'^i\s+like\s+\w+$',  # "i like play" (missing to)
            ]
            for pattern in malformed_patterns:
                if re.match(pattern, query, re.IGNORECASE):
                    text_to_correct = query
                    break
        
        if text_to_correct:
            try:
                correction = correct_grammar(text_to_correct)
                corrected_text = correction.get("corrected", text_to_correct)
                errors = correction.get("changes", [])
                
                if corrected_text != text_to_correct:
                    response = f"""✅ **Correction:**

**Original:** {text_to_correct}
**Corrected:** {corrected_text}

**What was fixed:**
"""
                    for error in errors[:3]:
                        error_type = error.get("type", "grammar")
                        response += f"• {error_type.replace('_', ' ').title()}\n"
                    
                    if len(errors) > 3:
                        response += f"• And {len(errors) - 3} more improvement(s)\n"
                else:
                    response = f"✅ Your sentence looks good! '{text_to_correct}' is grammatically correct."
                
                return {
                    "response": response,
                    "suggestions": ["Check another sentence", "Learn grammar rules", "Practice more"],
                    "type": "correction"
                }
            except Exception as e:
                return {
                    "response": f"I'd be happy to help correct your sentence! Could you write the sentence you'd like me to check?",
                    "suggestions": ["Example: 'I am student'", "Example: 'She go to school'"],
                    "type": "correction"
                }
        else:
            return {
                "response": "I can help you correct sentences! Just write the sentence you'd like me to check, and I'll provide corrections and explanations.",
                "suggestions": ["Example: 'I am student'", "Example: 'She go to school'"],
                "type": "correction"
            }
    
    # Handle specific grammar topics
    if intent["type"] == "grammar" and intent["subtopic"]:
        topic_info = KNOWLEDGE_BASE["grammar"].get(intent["subtopic"], {})
        if topic_info:
            response = topic_info.get("explanation", "")
            examples = topic_info.get("examples", [])
            
            if examples:
                response += "\n\n**Examples:**\n"
                for i, example in enumerate(examples[:3], 1):
                    response += f"{i}. {example}\n"
            
            return {
                "response": response,
                "suggestions": [
                    "More grammar topics",
                    "Practice exercises",
                    "Check my sentence"
                ],
                "type": "grammar_explanation"
            }
    
    # Handle vocabulary questions
    if intent["type"] == "vocabulary":
        # Try to extract the word
        words = query.split()
        potential_word = None
        for word in words:
            word_clean = re.sub(r'[^\w]', '', word.lower())
            if len(word_clean) > 3 and word_clean not in ["what", "does", "mean", "meaning", "definition"]:
                potential_word = word_clean
                break
        
        if potential_word:
            try:
                synonyms = suggest_synonyms(potential_word, "")
                if synonyms:
                    response = f"""**Word:** {potential_word.capitalize()}

**Synonyms:** {', '.join(synonyms[:5])}

Would you like me to explain how to use this word in sentences?"""
                else:
                    response = f"I can help you learn about '{potential_word}'! This word is commonly used in English. Would you like to see example sentences?"
                
                return {
                    "response": response,
                    "suggestions": [
                        "Show example sentences",
                        "Explain usage",
                        "More vocabulary help"
                    ],
                    "type": "vocabulary"
                }
            except:
                pass
        
        topic_info = KNOWLEDGE_BASE["vocabulary"].get(intent.get("subtopic", "word_meaning"), {})
        return {
            "response": topic_info.get("explanation", "I can help you with vocabulary! Tell me a word you'd like to learn about."),
            "suggestions": ["Word meanings", "Synonyms", "Example sentences"],
            "type": "vocabulary"
        }
    
    # Handle writing tips
    if intent["type"] == "writing":
        topic_info = KNOWLEDGE_BASE["writing"].get(intent.get("subtopic", "tips"), {})
        return {
            "response": topic_info.get("explanation", "I can help you improve your writing! What specific area would you like help with?"),
            "suggestions": ["Writing tips", "Style improvement", "Check my text"],
            "type": "writing"
        }
    
    # Handle questions (focused on grammar and EduLingua)
    if intent["is_question"]:
        if "how" in query.lower():
            return {
                "response": """Great question! I can help you understand English grammar better. Here are some ways I can help:

**Grammar Topics:**
• How to use articles (a, an, the)?
• How to form correct sentences?
• How to use tenses correctly?
• How to improve your grammar?

**EduLingua Features:**
• How to use the Dashboard for text analysis
• How to check grammar errors
• How to improve your writing

**Try asking:**
• "How do I use articles?"
• "How to check my grammar?"
• "How does the dashboard work?"

Or go to the Dashboard and type a sentence to see how it works!""",
                "suggestions": ["Explain grammar rules", "Use the dashboard", "Check my sentence"],
                "type": "question"
            }
        elif "what" in query.lower():
            return {
                "response": """I can explain English grammar rules, vocabulary, and help you use EduLingua features!

**Grammar Topics:**
• What are articles? (a, an, the)
• What is sentence structure?
• What are tenses?
• What are common grammar mistakes?

**EduLingua Features:**
• What does the Dashboard do? (Analyzes your text for grammar, vocabulary, readability)
• What is grammar correction? (Fixes errors and explains why)
• What is rephrasing? (Suggests better ways to write)

**Try asking:**
• "What are articles?"
• "What is the dashboard?"
• "What does [word] mean?"

Or use the Dashboard to analyze your text!""",
                "suggestions": ["Grammar rules", "Dashboard features", "Vocabulary help"],
                "type": "question"
            }
        elif "why" in query.lower():
            return {
                "response": """Understanding WHY grammar rules work helps you remember them better!

**I can explain:**
• Why we use certain grammar rules
• Why sentences are structured a certain way
• Why certain words are used in specific contexts
• Why corrections are made

**Try asking:**
• "Why do we use 'the' here?"
• "Why is this sentence wrong?"
• "Why is this correction better?"

Or check a sentence in the Dashboard to see detailed explanations!""",
                "suggestions": ["Grammar explanations", "Check my sentence", "Use the dashboard"],
                "type": "question"
            }
    
    # Default intelligent response (focused on grammar and EduLingua)
    return {
        "response": """I'm **EduLingua Pro**, your grammar tutor! I focus on helping you learn English grammar and improve your language skills.

**I can help you with:**

📚 **Grammar Rules & Corrections**
   - Articles (a, an, the)
   - Tenses (past, present, future)
   - Prepositions (in, on, at, etc.)
   - Sentence structure and word order
   - Common grammar mistakes

📖 **Vocabulary & Word Usage**
   - Word meanings and definitions
   - Synonyms and alternatives
   - Proper word usage in sentences

✍️ **Writing Improvement**
   - Grammar checking
   - Style and clarity tips
   - Sentence formation

**How to Use EduLingua:**
1. **Dashboard** - Type any text to get instant grammar analysis
2. **Ask Me** - Ask grammar questions or check sentences
3. **Practice** - Use dialog practice and exercises

**Try asking:**
• "Explain articles" or "What are articles?"
• "Check: I am student" or "Correct: name Nishanth I"
• "What does [word] mean?"
• "Help with sentence structure"

Or go to the **Dashboard** to analyze your text!""",
        "suggestions": [
            "Explain grammar rules",
            "Check my sentence",
            "Use the dashboard",
            "Help with vocabulary"
        ],
        "type": "general"
    }

