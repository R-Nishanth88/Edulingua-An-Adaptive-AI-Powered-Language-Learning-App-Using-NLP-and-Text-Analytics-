"""
Plagiarism & Repetition Detection - Ensures originality in written exercises.
"""
from typing import Dict, List, Tuple, Optional
from collections import Counter

def detect_plagiarism(text: str, reference_texts: Optional[List[str]] = None) -> Dict:
    """
    Detect potential plagiarism and repetition.
    
    Args:
        text: Text to check
        reference_texts: Reference texts to compare against (optional)
    
    Returns:
        Dictionary with plagiarism scores and matches
    """
    from core.semantic_similarity import calculate_semantic_similarity
    from core.preprocessing import preprocess_text
    
    results = {
        "originality_score": 100.0,
        "repetition_score": 0.0,
        "plagiarism_risk": "low",
        "matches": [],
        "repetitive_phrases": [],
        "recommendations": []
    }
    
    # Check internal repetition
    repetition_analysis = detect_internal_repetition(text)
    results["repetition_score"] = repetition_analysis["score"]
    results["repetitive_phrases"] = repetition_analysis["phrases"]
    results["originality_score"] -= repetition_analysis["score"] * 50
    
    # Check against reference texts if provided
    if reference_texts:
        plagiarism_matches = check_against_references(text, reference_texts)
        results["matches"] = plagiarism_matches
        if plagiarism_matches:
            max_similarity = max(match["similarity"] for match in plagiarism_matches)
            results["originality_score"] -= max_similarity * 50
            if max_similarity > 0.8:
                results["plagiarism_risk"] = "high"
            elif max_similarity > 0.6:
                results["plagiarism_risk"] = "medium"
    
    # Generate recommendations
    if results["repetition_score"] > 0.3:
        results["recommendations"].append("Reduce repetitive phrases. Use synonyms and varied expressions.")
    
    if results["originality_score"] < 70:
        results["recommendations"].append("Ensure your writing is original. Paraphrase any borrowed ideas.")
    
    results["originality_score"] = max(0, min(100, results["originality_score"]))
    
    return results

def detect_internal_repetition(text: str) -> Dict:
    """
    Detect repetition within the text itself.
    """
    from core.preprocessing import preprocess_text
    
    preprocessed = preprocess_text(text)
    sentences = preprocessed.get("sentences", [])
    
    if len(sentences) < 2:
        return {
            "score": 0.0,
            "phrases": []
        }
    
    # Check for repeated phrases (3+ words)
    all_phrases = []
    for sentence in sentences:
        words = sentence.lower().split()
        for i in range(len(words) - 2):
            phrase = " ".join(words[i:i+3])
            all_phrases.append(phrase)
    
    phrase_counts = Counter(all_phrases)
    repeated_phrases = [(phrase, count) for phrase, count in phrase_counts.items() if count > 1]
    
    # Calculate repetition score
    total_phrases = len(all_phrases)
    repeated_count = sum(count - 1 for _, count in repeated_phrases)  # Count extra occurrences
    repetition_score = repeated_count / total_phrases if total_phrases > 0 else 0.0
    
    return {
        "score": round(repetition_score, 3),
        "phrases": [{"phrase": phrase, "count": count} for phrase, count in repeated_phrases[:10]]
    }

def check_against_references(text: str, reference_texts: List[str]) -> List[Dict]:
    """
    Check text against reference texts for potential plagiarism.
    """
    from core.semantic_similarity import calculate_semantic_similarity
    
    matches = []
    
    for i, ref_text in enumerate(reference_texts):
        similarity = calculate_semantic_similarity(text, ref_text)
        
        if similarity > 0.5:  # Threshold for potential match
            matches.append({
                "reference_index": i,
                "similarity": round(similarity * 100, 1),
                "risk_level": "high" if similarity > 0.8 else "medium" if similarity > 0.6 else "low",
                "excerpt": ref_text[:100] + "..." if len(ref_text) > 100 else ref_text
            })
    
    # Sort by similarity
    matches.sort(key=lambda x: x["similarity"], reverse=True)
    
    return matches

def detect_exact_matches(text: str, reference_texts: Optional[List[str]] = None) -> List[Dict]:
    """
    Detect exact or near-exact text matches.
    """
    matches = []
    
    # Check for exact sentence matches
    from core.preprocessing import preprocess_text
    preprocessed = preprocess_text(text)
    sentences = preprocessed.get("sentences", [])
    
    if reference_texts:
        for ref_text in reference_texts:
            ref_preprocessed = preprocess_text(ref_text)
            ref_sentences = ref_preprocessed.get("sentences", [])
            
            for sent in sentences:
                for ref_sent in ref_sentences:
                    # Check for exact or near-exact matches
                    similarity = calculate_word_overlap(sent, ref_sent)
                    if similarity > 0.9:
                        matches.append({
                            "type": "exact_match",
                            "sentence": sent,
                            "reference_sentence": ref_sent,
                            "similarity": round(similarity * 100, 1)
                        })
    
    return matches

def calculate_word_overlap(text1: str, text2: str) -> float:
    """Calculate word overlap between two texts."""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

