from typing import List, Dict
import re

# Try to import transformers (optional)
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    pipeline = None

# Initialize summarization pipeline (optional)
summarizer = None
if TRANSFORMERS_AVAILABLE:
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
    except Exception as e:
        print(f"Warning: Could not load summarization model: {e}")
        summarizer = None

def summarize_text(text: str, max_length: int = 150, min_length: int = 50) -> Dict:
    """
    Summarize text using BART or T5 model.
    """
    if not text or len(text.split()) < 20:
        return {
            "summary": text,
            "original_length": len(text.split()),
            "summary_length": len(text.split()),
            "compression_ratio": 1.0
        }
    
    try:
        if summarizer:
            result = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            summary = result[0]["summary_text"]
        else:
            # Fallback: simple extractive summarization (first few sentences)
            sentences = text.split('.')
            summary = '. '.join(sentences[:3]) + '.'
    except Exception as e:
        print(f"Error in summarization: {e}")
        # Fallback
        sentences = text.split('.')
        summary = '. '.join(sentences[:3]) + '.'
    
    original_length = len(text.split())
    summary_length = len(summary.split())
    compression_ratio = summary_length / original_length if original_length > 0 else 1.0
    
    return {
        "summary": summary,
        "original_length": original_length,
        "summary_length": summary_length,
        "compression_ratio": round(compression_ratio, 3)
    }

def generate_questions(text: str, num_questions: int = 5) -> List[Dict]:
    """
    Generate comprehension questions from text.
    Uses rule-based approach (can be enhanced with T5 QG model).
    """
    if not text:
        return []
    
    questions = []
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Simple question generation based on sentence structure
    # In production, use T5 question generation model
    question_templates = [
        "What is the main idea of this text?",
        "What are the key points discussed?",
        "Can you summarize the main argument?",
        "What details support the main idea?",
        "What conclusion can be drawn from this text?"
    ]
    
    # Generate questions based on sentences
    for i, template in enumerate(question_templates[:num_questions]):
        questions.append({
            "question": template,
            "type": "comprehension",
            "difficulty": "medium",
            "hint": "Review the main sentences in the text."
        })
    
    # Generate specific questions from sentences
    for sentence in sentences[:min(3, len(sentences))]:
        if len(sentence.split()) > 5:
            # Simple transformation (can be improved)
            words = sentence.split()
            if words[0].lower() in ["the", "a", "an", "this", "that"]:
                question = f"What is {sentence.lower()}?"
            else:
                question = f"Can you explain: {sentence}?"
            
            questions.append({
                "question": question,
                "type": "detail",
                "difficulty": "medium",
                "hint": "Look for this information in the text."
            })
    
    return questions[:num_questions]
