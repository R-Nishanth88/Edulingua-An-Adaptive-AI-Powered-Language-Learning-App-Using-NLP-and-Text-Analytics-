"""
Grammar Explanation Engine using LanguageTool and rule-based explanations.
Provides detailed explanations for grammar corrections.
"""
from typing import List, Dict, Optional
import re

# Try to import language_tool_python
try:
    import language_tool_python
    LANGUAGE_TOOL_AVAILABLE = True
except ImportError:
    LANGUAGE_TOOL_AVAILABLE = False
    language_tool_python = None

# Global LanguageTool instance
language_tool = None

def load_language_tool():
    """Lazy load LanguageTool."""
    global language_tool
    
    if not LANGUAGE_TOOL_AVAILABLE:
        return False
    
    if language_tool is not None:
        return True
    
    try:
        language_tool = language_tool_python.LanguageTool('en-US')
        print("✅ LanguageTool loaded")
        return True
    except Exception as e:
        print(f"⚠️ Could not load LanguageTool: {e}")
        return False

def explain_correction(original: str, corrected: str, detailed: bool = True) -> Dict:
    """
    Explain grammar corrections with detailed error analysis.
    
    Args:
        original: Original text with errors
        corrected: Corrected text
        detailed: Whether to provide detailed explanations
    
    Returns:
        Dictionary with explanations, errors, and suggestions
    """
    explanations = []
    errors = []
    suggestions = []
    
    if not original or not original.strip():
        return {
            "summary": "No text provided.",
            "explanations": [],
            "errors": [],
            "suggestions": []
        }
    
    # Use LanguageTool if available
    if LANGUAGE_TOOL_AVAILABLE and load_language_tool():
        try:
            matches = language_tool.check(original)
            for match in matches:
                error_info = {
                    "error": match.message,
                    "suggestions": match.replacements[:3] if match.replacements else [],
                    "context": match.context,
                    "offset": match.offset,
                    "errorLength": match.errorLength,
                    "rule_id": match.ruleId,
                    "category": match.category
                }
                errors.append(error_info)
                explanations.append({
                    "type": "language_tool",
                    "message": match.message,
                    "suggestions": match.replacements[:3] if match.replacements else [],
                    "rule": match.ruleId
                })
        except Exception as e:
            print(f"⚠️ Error using LanguageTool: {e}")
    
    # Add rule-based explanations
    rule_based = generate_rule_based_explanations(original, corrected)
    explanations.extend(rule_based)
    
    # Generate summary
    if original != corrected:
        summary = generate_correction_summary(original, corrected, errors)
    else:
        summary = "Your sentence is grammatically correct."
    
    # Extract suggestions from explanations
    for exp in explanations:
        if "suggestions" in exp and exp["suggestions"]:
            suggestions.extend(exp["suggestions"][:2])  # Limit to 2 per explanation
    
    return {
        "summary": summary,
        "explanations": explanations,
        "errors": errors,
        "suggestions": list(set(suggestions))[:5],  # Unique suggestions, max 5
        "correction_applied": original != corrected
    }

def generate_rule_based_explanations(original: str, corrected: str) -> List[Dict]:
    """
    Generate rule-based explanations for common errors.
    """
    explanations = []
    
    original_lower = original.lower()
    corrected_lower = corrected.lower()
    
    # Check for word order changes
    if "my name is" in corrected_lower and "i" in original_lower and "name" in original_lower:
        if "my name is" not in original_lower:
            explanations.append({
                "type": "word_order",
                "message": "Sentence structure corrected: English follows Subject-Verb-Object order.",
                "rule": "English sentence structure: 'My name is [name]' is the standard format.",
                "example": f"❌ '{original}' → ✅ '{corrected}'"
            })
    
    # Check for missing articles
    if "i am a" in corrected_lower or "i am an" in corrected_lower:
        if "i am a" not in original_lower and "i am an" not in original_lower:
            explanations.append({
                "type": "missing_article",
                "message": "Added article 'a' or 'an' before the noun.",
                "rule": "Use 'a' before consonant sounds, 'an' before vowel sounds.",
                "example": "I am student → I am a student"
            })
    
    # Check for missing infinitives
    if "to" in corrected_lower and "to" not in original_lower:
        if any(verb in original_lower for verb in ["like", "want", "need", "try"]):
            explanations.append({
                "type": "missing_infinitive",
                "message": "Added 'to' before the verb to form an infinitive.",
                "rule": "After verbs like 'like', 'want', 'need', use 'to' + base verb.",
                "example": "I like play → I like to play"
            })
    
    # Check for capitalization
    if corrected[0].isupper() and original[0].islower():
        explanations.append({
            "type": "capitalization",
            "message": "Capitalized the first letter of the sentence.",
            "rule": "Sentences must begin with a capital letter.",
            "example": f"'{original}' → '{corrected}'"
        })
    
    # Check for punctuation
    if corrected.endswith('.') and not original.endswith('.'):
        explanations.append({
            "type": "punctuation",
            "message": "Added period at the end of the sentence.",
            "rule": "Declarative sentences end with a period.",
            "example": f"'{original}' → '{corrected}'"
        })
    
    return explanations

def generate_correction_summary(original: str, corrected: str, errors: List[Dict]) -> str:
    """
    Generate a human-readable summary of corrections.
    """
    if not errors and original == corrected:
        return "Your sentence is grammatically correct."
    
    summary_parts = []
    
    # Count error types
    error_types = {}
    for error in errors:
        category = error.get("category", "general")
        error_types[category] = error_types.get(category, 0) + 1
    
    if error_types:
        if "GRAMMAR" in str(error_types):
            summary_parts.append("Fixed grammatical errors")
        if "TYPOS" in str(error_types):
            summary_parts.append("Corrected spelling mistakes")
        if "STYLE" in str(error_types):
            summary_parts.append("Improved writing style")
    
    # Add structure changes
    if "my name is" in corrected.lower() and "my name is" not in original.lower():
        summary_parts.append("Restructured sentence to follow English word order")
    
    if "to" in corrected.lower() and "to" not in original.lower():
        summary_parts.append("Added missing infinitive marker 'to'")
    
    if any(article in corrected.lower() for article in [" a ", " an "]) and \
       not any(article in original.lower() for article in [" a ", " an "]):
        summary_parts.append("Added missing articles")
    
    if summary_parts:
        return " | ".join(summary_parts) + "."
    else:
        return "Rephrased to follow standard English syntax and subject-verb order."

def get_grammar_rule(error_type: str) -> str:
    """
    Get explanation for a specific grammar rule.
    """
    rules = {
        "word_order": "English sentences follow Subject-Verb-Object (SVO) order. Example: 'My name is John' not 'Name John I'.",
        "missing_article": "Use 'a' before consonant sounds (a book), 'an' before vowel sounds (an apple).",
        "missing_infinitive": "After verbs like 'like', 'want', 'need', use 'to' + base verb: 'I like to play'.",
        "subject_verb_agreement": "Subject and verb must agree in number: 'I am' not 'I is', 'They are' not 'They is'.",
        "capitalization": "Always capitalize the first letter of a sentence and proper nouns.",
        "punctuation": "End declarative sentences with a period (.), questions with (?), exclamations with (!).",
        "spelling": "Check spelling of words. Use a dictionary or spell-checker for unfamiliar words."
    }
    
    return rules.get(error_type, "Follow standard English writing conventions.")

