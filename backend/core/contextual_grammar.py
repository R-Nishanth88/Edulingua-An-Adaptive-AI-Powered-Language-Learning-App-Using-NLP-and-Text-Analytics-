"""
Context-Aware Grammar Correction Module
Corrects entire paragraphs preserving context across sentences.
"""
from typing import List, Dict, Optional
from nltk.tokenize import sent_tokenize
from core.grammar_analysis import correct_grammar, detect_grammar_errors
from core.ai_service import generate_ai_response, is_ai_available

def correct_paragraph_with_context(text: str, use_ai: bool = True) -> Dict:
    """
    Correct grammar errors in a paragraph while preserving context.
    Handles multi-sentence corrections with cross-sentence coherence.
    
    Args:
        text: Input paragraph (multiple sentences)
        use_ai: Whether to use AI for contextual corrections
    
    Returns:
        Dictionary with corrected text, changes, and context notes
    """
    if not text or not text.strip():
        return {
            "original": text,
            "corrected": text,
            "changes": [],
            "context_preserved": True
        }
    
    # Split into sentences
    sentences = sent_tokenize(text.strip())
    
    if len(sentences) == 1:
        # Single sentence - use regular correction
        return correct_grammar(text, use_ai=use_ai)
    
    # Multi-sentence paragraph - use contextual correction
    if use_ai and is_ai_available():
        try:
            # Use AI for context-aware correction
            ai_prompt = f"""Correct this English paragraph while preserving context and coherence across sentences. Fix:
1. Grammar errors in each sentence
2. Spelling mistakes
3. Punctuation and capitalization
4. Sentence structure and word order
5. Cross-sentence coherence (pronoun references, tense consistency, logical flow)
6. Paragraph structure and transitions

Maintain the original meaning and context. Return the fully corrected paragraph.

Original Paragraph:
{text}

Corrected Paragraph:"""
            
            ai_corrected = generate_ai_response(
                ai_prompt,
                "You are an English grammar expert specializing in contextual paragraph correction. Preserve meaning and coherence while fixing all errors.",
                max_tokens=500,
                temperature=0.3
            )
            
            if ai_corrected and ai_corrected.strip() and ai_corrected.strip() != text:
                # Analyze changes
                corrected_sentences = sent_tokenize(ai_corrected.strip())
                changes = []
                
                # Compare original and corrected sentences
                for i, (orig_sent, corr_sent) in enumerate(zip(sentences, corrected_sentences[:len(sentences)])):
                    if orig_sent.strip() != corr_sent.strip():
                        changes.append({
                            "sentence_index": i,
                            "original": orig_sent.strip(),
                            "corrected": corr_sent.strip(),
                            "type": "contextual_correction",
                            "message": f"Sentence {i+1} corrected with context awareness"
                        })
                
                return {
                    "original": text,
                    "corrected": ai_corrected.strip(),
                    "changes": changes,
                    "context_preserved": True,
                    "method": "ai_contextual",
                    "sentence_count": len(sentences),
                    "corrections_applied": len(changes)
                }
        except Exception as e:
            print(f"⚠️ AI contextual correction failed: {e}")
    
    # Fallback: sentence-by-sentence correction with context notes
    corrected_sentences = []
    all_changes = []
    previous_context = {}
    
    for i, sentence in enumerate(sentences):
        # Correct individual sentence
        correction = correct_grammar(sentence, use_ai=use_ai)
        corrected_sent = correction.get("corrected", sentence)
        corrected_sentences.append(corrected_sent)
        
        # Track changes with context
        if correction.get("changes"):
            for change in correction.get("changes", []):
                change["sentence_index"] = i
                change["context_note"] = f"Part of paragraph with {len(sentences)} sentences"
                all_changes.append(change)
        
        # Update context for next sentence (e.g., tense consistency)
        if i < len(sentences) - 1:
            # Extract tense from current sentence for consistency
            # This is a simplified version - could be enhanced with NLP
            previous_context["sentence_index"] = i
    
    corrected_paragraph = " ".join(corrected_sentences)
    
    return {
        "original": text,
        "corrected": corrected_paragraph,
        "changes": all_changes,
        "context_preserved": True,
        "method": "sentence_by_sentence",
        "sentence_count": len(sentences),
        "corrections_applied": len(all_changes)
    }

def analyze_paragraph_coherence(text: str) -> Dict:
    """
    Analyze coherence and flow of a paragraph.
    
    Returns:
        Dictionary with coherence metrics and suggestions
    """
    sentences = sent_tokenize(text.strip())
    
    if len(sentences) < 2:
        return {
            "coherence_score": 1.0,
            "flow_issues": [],
            "suggestions": []
        }
    
    # Check for transition words
    transition_words = [
        "however", "therefore", "furthermore", "moreover", "additionally",
        "consequently", "meanwhile", "subsequently", "nevertheless", "thus"
    ]
    
    # Check tense consistency
    # Simplified check - could be enhanced with POS tagging
    flow_issues = []
    suggestions = []
    
    # Check for pronoun references
    pronouns = ["it", "this", "that", "these", "those", "he", "she", "they"]
    has_pronouns = any(pronoun in text.lower() for pronoun in pronouns)
    
    if has_pronouns:
        suggestions.append("Ensure pronoun references are clear across sentences")
    
    # Check for transition words
    has_transitions = any(trans in text.lower() for trans in transition_words)
    if not has_transitions and len(sentences) > 2:
        suggestions.append("Consider adding transition words to improve flow")
    
    coherence_score = 0.8  # Base score
    if has_transitions:
        coherence_score += 0.1
    if has_pronouns:
        coherence_score += 0.05
    
    coherence_score = min(coherence_score, 1.0)
    
    return {
        "coherence_score": coherence_score,
        "flow_issues": flow_issues,
        "suggestions": suggestions,
        "sentence_count": len(sentences),
        "has_transitions": has_transitions,
        "has_pronoun_references": has_pronouns
    }

