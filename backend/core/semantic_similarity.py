"""
Semantic Similarity Scoring - Compares learner-written sentences with target answers.
"""
from typing import Dict, List, Tuple
import numpy as np

# Try to import sentence transformers
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None

# Global model
sbert_model = None

def load_similarity_model():
    """Lazy load sentence transformer model."""
    global sbert_model
    
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        return False
    
    if sbert_model is not None:
        return True
    
    try:
        sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Semantic similarity model loaded")
        return True
    except Exception as e:
        print(f"⚠️ Could not load similarity model: {e}")
        return False

def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity between two texts (0-1).
    
    Args:
        text1: First text (learner's answer)
        text2: Second text (target answer)
    
    Returns:
        Similarity score (0-1, where 1 is identical meaning)
    """
    if not text1 or not text2:
        return 0.0
    
    if text1.lower().strip() == text2.lower().strip():
        return 1.0
    
    # Use sentence transformers if available
    if SENTENCE_TRANSFORMERS_AVAILABLE and load_similarity_model():
        try:
            embeddings = sbert_model.encode([text1, text2])
            similarity = np.dot(embeddings[0], embeddings[1]) / (
                np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
            )
            return float(similarity)
        except Exception as e:
            print(f"Error calculating semantic similarity: {e}")
    
    # Fallback: Simple word overlap
    return calculate_word_overlap(text1, text2)

def calculate_word_overlap(text1: str, text2: str) -> float:
    """Calculate word overlap similarity (fallback)."""
    from core.preprocessing import preprocess_text
    
    preprocessed1 = preprocess_text(text1)
    preprocessed2 = preprocess_text(text2)
    
    words1 = set(preprocessed1.get("tokens", []))
    words2 = set(preprocessed2.get("tokens", []))
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    jaccard_similarity = len(intersection) / len(union) if union else 0.0
    return round(jaccard_similarity, 3)

def compare_with_target(learner_answer: str, target_answer: str) -> Dict:
    """
    Compare learner's answer with target answer.
    
    Args:
        learner_answer: Learner's written answer
        target_answer: Expected/correct answer
    
    Returns:
        Dictionary with similarity score and feedback
    """
    similarity = calculate_semantic_similarity(learner_answer, target_answer)
    
    # Determine feedback based on similarity
    if similarity >= 0.9:
        feedback = "Excellent! Your answer matches the target meaning very closely."
        grade = "A"
    elif similarity >= 0.7:
        feedback = "Good! Your answer is close to the target, with minor differences."
        grade = "B"
    elif similarity >= 0.5:
        feedback = "Fair. Your answer captures some of the meaning but needs improvement."
        grade = "C"
    elif similarity >= 0.3:
        feedback = "Needs work. Your answer is somewhat related but misses key points."
        grade = "D"
    else:
        feedback = "Try again. Your answer doesn't match the expected meaning."
        grade = "F"
    
    return {
        "similarity_score": round(similarity * 100, 1),
        "grade": grade,
        "feedback": feedback,
        "learner_answer": learner_answer,
        "target_answer": target_answer,
        "key_differences": identify_key_differences(learner_answer, target_answer) if similarity < 0.8 else []
    }

def identify_key_differences(text1: str, text2: str) -> List[str]:
    """Identify key differences between texts."""
    from core.preprocessing import preprocess_text
    
    preprocessed1 = preprocess_text(text1)
    preprocessed2 = preprocess_text(text2)
    
    words1 = set(preprocessed1.get("tokens", []))
    words2 = set(preprocessed2.get("tokens", []))
    
    missing_words = words2 - words1
    extra_words = words1 - words2
    
    differences = []
    if missing_words:
        differences.append(f"Missing key words: {', '.join(list(missing_words)[:5])}")
    if extra_words:
        differences.append(f"Extra words: {', '.join(list(extra_words)[:5])}")
    
    return differences
