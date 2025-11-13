"""
Long Text Summarizer + Reviewer Module
Summarizes essays and provides improvement points.
"""
from typing import Dict, List, Optional
from core.ai_service import generate_ai_response, is_ai_available
from core.grammar_analysis import detect_grammar_errors, correct_grammar
from core.writing_quality_score import calculate_writing_quality_score
from core.readability import calculate_readability
from core.lexical_semantic import calculate_lexical_diversity

def summarize_and_review(text: str, use_ai: bool = True) -> Dict:
    """
    Summarize long text and provide improvement points.
    
    Args:
        text: Input text (essay/article) to summarize and review
        use_ai: Whether to use AI for summarization
    
    Returns:
        Dictionary with summary, key points, and improvement suggestions
    """
    if not text or len(text.strip()) < 50:
        return {
            "summary": "",
            "key_points": [],
            "improvements": [],
            "word_count": 0,
            "error": "Text must be at least 50 characters"
        }
    
    word_count = len(text.split())
    sentences = text.split('.')
    sentence_count = len([s for s in sentences if s.strip()])
    
    # Analyze the text
    grammar_errors = detect_grammar_errors(text)
    quality_score = calculate_writing_quality_score(text, use_ai=use_ai)
    readability = calculate_readability(text)
    
    # Generate summary using AI
    summary = ""
    if use_ai and is_ai_available():
        try:
            prompt = f"""Summarize this text in 2-3 sentences, capturing the main ideas:

{text}

Summary:"""
            
            summary = generate_ai_response(
                prompt,
                "You are a text summarization expert. Create concise, accurate summaries.",
                max_tokens=150,
                temperature=0.5
            )
        except Exception as e:
            print(f"⚠️ AI summarization failed: {e}")
    
    # Fallback: extract first and last sentences
    if not summary:
        if sentence_count >= 2:
            summary = f"{sentences[0].strip()}. {sentences[-1].strip()}."
        else:
            summary = text[:200] + "..." if len(text) > 200 else text
    
    # Extract key points
    key_points = extract_key_points(text, use_ai=use_ai)
    
    # Generate improvement suggestions
    improvements = generate_improvement_suggestions(
        text,
        grammar_errors,
        quality_score,
        readability,
        use_ai=use_ai
    )
    
    return {
        "summary": summary.strip(),
        "key_points": key_points,
        "improvements": improvements,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "quality_score": quality_score.get("overall_score", 0),
        "grammar_errors": len(grammar_errors),
        "readability": readability
    }

def extract_key_points(text: str, use_ai: bool = True) -> List[str]:
    """Extract key points from the text."""
    if use_ai and is_ai_available():
        try:
            prompt = f"""Extract 3-5 key points from this text. List them as bullet points:

{text}

Key Points:"""
            
            key_points_text = generate_ai_response(
                prompt,
                "You are an expert at extracting key information from text.",
                max_tokens=200,
                temperature=0.4
            )
            
            if key_points_text:
                # Parse bullet points
                points = [p.strip() for p in key_points_text.split('\n') if p.strip() and (p.strip().startswith('-') or p.strip().startswith('•') or p.strip()[0].isdigit())]
                # Clean up bullet markers
                points = [p.lstrip('- •0123456789. ').strip() for p in points if len(p.strip()) > 10]
                if points:
                    return points[:5]
        except Exception as e:
            print(f"⚠️ Key points extraction failed: {e}")
    
    # Fallback: extract sentences with important words
    sentences = text.split('.')
    important_words = ['important', 'key', 'main', 'primary', 'essential', 'crucial', 'significant']
    key_points = []
    for sentence in sentences[:5]:
        if any(word in sentence.lower() for word in important_words) and len(sentence.strip()) > 20:
            key_points.append(sentence.strip() + '.')
    
    return key_points[:5] if key_points else [sentences[0].strip() + '.'] if sentences else []

def generate_improvement_suggestions(
    text: str,
    grammar_errors: List[Dict],
    quality_score: Dict,
    readability: Dict,
    use_ai: bool = True
) -> List[Dict]:
    """Generate specific improvement suggestions."""
    improvements = []
    
    # Grammar improvements
    if len(grammar_errors) > 0:
        error_types = {}
        for error in grammar_errors:
            error_type = error.get("type", "general")
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        most_common = max(error_types.items(), key=lambda x: x[1]) if error_types else None
        if most_common:
            improvements.append({
                "category": "Grammar",
                "priority": "high",
                "suggestion": f"Fix {most_common[1]} {most_common[0]} error(s). Focus on improving this area.",
                "error_type": most_common[0],
                "count": most_common[1]
            })
    
    # Quality score improvements
    components = quality_score.get("components", {})
    
    if components.get("grammar_correctness", {}).get("score", 100) < 70:
        improvements.append({
            "category": "Grammar",
            "priority": "high",
            "suggestion": "Improve grammar correctness. Review subject-verb agreement, tense consistency, and sentence structure.",
            "current_score": components.get("grammar_correctness", {}).get("score", 0)
        })
    
    if components.get("clarity_readability", {}).get("score", 100) < 70:
        improvements.append({
            "category": "Clarity",
            "priority": "medium",
            "suggestion": "Improve clarity and readability. Simplify complex sentences and use clearer language.",
            "current_score": components.get("clarity_readability", {}).get("score", 0)
        })
    
    if components.get("coherence_flow", {}).get("score", 100) < 70:
        improvements.append({
            "category": "Coherence",
            "priority": "medium",
            "suggestion": "Improve coherence and flow. Add transition words and ensure logical connections between ideas.",
            "current_score": components.get("coherence_flow", {}).get("score", 0)
        })
    
    if components.get("vocabulary_style", {}).get("score", 100) < 70:
        improvements.append({
            "category": "Vocabulary",
            "priority": "low",
            "suggestion": "Enhance vocabulary diversity. Use more varied and precise word choices.",
            "current_score": components.get("vocabulary_style", {}).get("score", 0)
        })
    
    # AI-generated specific suggestions
    if use_ai and is_ai_available() and improvements:
        try:
            prompt = f"""Based on this writing analysis, provide 2-3 specific, actionable improvement suggestions:

Text: {text[:500]}

Issues found:
{chr(10).join([f"- {imp['category']}: {imp['suggestion']}" for imp in improvements[:3]])}

Provide specific, actionable suggestions:"""
            
            ai_suggestions = generate_ai_response(
                prompt,
                "You are a writing tutor providing specific, actionable feedback.",
                max_tokens=200,
                temperature=0.6
            )
            
            if ai_suggestions:
                # Add AI suggestions as additional improvements
                improvements.append({
                    "category": "AI Suggestions",
                    "priority": "medium",
                    "suggestion": ai_suggestions,
                    "source": "ai_enhanced"
                })
        except Exception as e:
            print(f"⚠️ AI improvement suggestions failed: {e}")
    
    return improvements[:5]  # Limit to top 5
