from typing import Dict, List
from collections import Counter
from textstat import syllable_count
import numpy as np

# Try to import sentence_transformers (optional)
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None

# Load Sentence-BERT model for semantic analysis (optional)
sbert_model = None
if SENTENCE_TRANSFORMERS_AVAILABLE:
    try:
        sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        print(f"Warning: Could not load Sentence-BERT model: {e}")
        sbert_model = None

def calculate_lexical_diversity(tokens: List[str]) -> Dict:
    """
    Calculate lexical diversity metrics: TTR, vocabulary richness, etc.
    """
    if not tokens:
        return {
            "ttr": 0.0,
            "unique_words": 0,
            "total_words": 0,
            "vocabulary_richness": 0.0,
            "avg_word_length": 0.0,
            "word_frequency": {}
        }
    
    total_words = len(tokens)
    unique_words = len(set(tokens))
    ttr = unique_words / total_words if total_words > 0 else 0.0
    
    # Word frequency distribution
    word_freq = Counter(tokens)
    
    # Average word length
    avg_word_length = sum(len(word) for word in tokens) / total_words if total_words > 0 else 0.0
    
    # Vocabulary richness (unique words per 100 words)
    vocabulary_richness = (unique_words / total_words * 100) if total_words > 0 else 0.0
    
    return {
        "ttr": round(ttr, 3),
        "unique_words": unique_words,
        "total_words": total_words,
        "vocabulary_richness": round(vocabulary_richness, 2),
        "avg_word_length": round(avg_word_length, 2),
        "word_frequency": dict(word_freq.most_common(20))
    }

def suggest_synonyms(word: str, context: str = "") -> List[Dict]:
    """
    Suggest synonyms and alternative words using semantic similarity.
    """
    suggestions = []
    
    # Basic synonym suggestions (can be enhanced with WordNet or API)
    basic_synonyms = {
        "good": ["excellent", "great", "wonderful", "fantastic", "superb"],
        "bad": ["poor", "terrible", "awful", "horrible", "dreadful"],
        "big": ["large", "huge", "enormous", "massive", "gigantic"],
        "small": ["tiny", "little", "mini", "petite", "minuscule"],
        "important": ["significant", "crucial", "vital", "essential", "key"],
        "nice": ["pleasant", "lovely", "delightful", "charming", "agreeable"],
    }
    
    word_lower = word.lower()
    if word_lower in basic_synonyms:
        for synonym in basic_synonyms[word_lower]:
            suggestions.append({
                "word": synonym,
                "similarity": 0.8,
                "example": f"Use '{synonym}' instead of '{word}' for more variety."
            })
    
    # Use Sentence-BERT for contextual suggestions if available
    if sbert_model and context:
        try:
            # This is a simplified version - can be enhanced
            pass
        except Exception as e:
            print(f"Error in semantic similarity: {e}")
    
    return suggestions[:5]  # Return top 5 suggestions

def extract_keywords(text: str, top_n: int = 10) -> List[Dict]:
    """
    Extract keywords using TF-IDF-like approach and NER.
    """
    from core.preprocessing import preprocess_text
    
    preprocessed = preprocess_text(text)
    tokens = preprocessed["tokens"]
    
    if not tokens:
        return []
    
    # Calculate term frequency
    word_freq = Counter(tokens)
    total_words = len(tokens)
    
    # Simple TF-IDF (without IDF since we don't have corpus)
    keywords = []
    for word, freq in word_freq.most_common(top_n * 2):
        if len(word) > 3:  # Filter short words
            tf = freq / total_words
            keywords.append({
                "word": word,
                "frequency": freq,
                "tf_score": round(tf, 4),
                "importance": "high" if tf > 0.02 else "medium"
            })
    
    # Include named entities
    entities = preprocessed.get("entities", [])
    for entity in entities[:5]:
        keywords.append({
            "word": entity["text"],
            "frequency": 1,
            "tf_score": 0.01,
            "importance": "high",
            "type": entity["label"]
        })
    
    return keywords[:top_n]

def analyze_semantic_coherence(text: str) -> Dict:
    """
    Analyze semantic coherence and topic consistency.
    """
    from core.preprocessing import preprocess_text
    
    preprocessed = preprocess_text(text)
    sentences = preprocessed["sentences"]
    
    if len(sentences) < 2:
        return {
            "coherence_score": 0.5,
            "topic_consistency": "low",
            "analysis": "Not enough sentences for coherence analysis"
        }
    
    # Use Sentence-BERT to calculate sentence similarity
    coherence_scores = []
    if sbert_model:
        try:
            embeddings = sbert_model.encode(sentences)
            for i in range(len(embeddings) - 1):
                similarity = np.dot(embeddings[i], embeddings[i+1]) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[i+1])
                )
                coherence_scores.append(float(similarity))
        except Exception as e:
            print(f"Error in coherence analysis: {e}")
    
    avg_coherence = np.mean(coherence_scores) if coherence_scores else 0.5
    
    return {
        "coherence_score": round(avg_coherence, 3),
        "topic_consistency": "high" if avg_coherence > 0.7 else "medium" if avg_coherence > 0.5 else "low",
        "sentence_similarities": [round(s, 3) for s in coherence_scores[:5]]
    }
