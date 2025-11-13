import re
from typing import List, Dict
from textblob import TextBlob
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from .sentence_structure import analyze_sentence_structure, correct_sentence_structure

# Try to import spaCy (optional)
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    spacy = None

# Try to import transformers (optional)
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    pipeline = None

# Load spaCy model (optional)
nlp = None
if SPACY_AVAILABLE:
    try:
        nlp = spacy.load("en_core_web_sm")
    except (OSError, IOError):
        nlp = None

# Initialize grammar correction pipeline (T5 model) - optional
corrector = None
if TRANSFORMERS_AVAILABLE:
    try:
        corrector = pipeline("text2text-generation", model="t5-base", device=-1)
    except Exception as e:
        print(f"Warning: Could not load T5 model: {e}")
        corrector = None

def detect_grammar_errors(text: str) -> List[Dict]:
    """
    Enhanced grammar error detection including sentence formation errors.
    Returns list of errors with positions, suggestions, and corrections.
    """
    errors = []
    
    if not text or not text.strip():
        return errors
    
    # First, analyze sentence structure
    structure_analysis = analyze_sentence_structure(text)
    structure_errors = structure_analysis.get("errors", [])
    errors.extend(structure_errors)
    
    # Rule-based checks for common mistakes
    common_mistakes = {
        r'\b(your|you\'re)\b.*\b(your|you\'re)\b': {
            "message": "Check usage of 'your' vs 'you're'",
            "correction": "Use 'your' for possession, 'you're' for 'you are'"
        },
        r'\b(its|it\'s)\b.*\b(its|it\'s)\b': {
            "message": "Check usage of 'its' vs 'it's'",
            "correction": "Use 'its' for possession, 'it's' for 'it is'"
        },
        r'\b(their|they\'re|there)\b.*\b(their|they\'re|there)\b': {
            "message": "Check usage of 'their', 'they're', or 'there'",
            "correction": "Use 'their' for possession, 'they're' for 'they are', 'there' for location"
        },
        r'\b(could of|should of|would of)\b': {
            "message": "Incorrect: 'could of', 'should of', 'would of'",
            "correction": "Use 'could have', 'should have', 'would have'"
        },
        r'\b(loose|lose)\b': {
            "message": "Check 'loose' (not tight) vs 'lose' (misplace)",
            "correction": "Use 'lose' when you misplace something, 'loose' when something is not tight"
        },
        r'\b(affect|effect)\b': {
            "message": "Check 'affect' (verb) vs 'effect' (noun)",
            "correction": "Use 'affect' as a verb (to influence), 'effect' as a noun (result)"
        },
        r'\b(then|than)\b': {
            "message": "Check 'then' (time) vs 'than' (comparison)",
            "correction": "Use 'then' for time sequence, 'than' for comparisons"
        },
    }
    
    for pattern, info in common_mistakes.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            errors.append({
                "type": "common_mistake",
                "message": info["message"],
                "start": match.start(),
                "end": match.end(),
                "text": match.group(),
                "correction": info["correction"],
                "severity": "medium"
            })
    
    # Check for double spaces
    double_space_matches = re.finditer(r'\s{2,}', text)
    for match in double_space_matches:
        errors.append({
            "type": "formatting",
            "message": "Double space detected",
            "start": match.start(),
            "end": match.end(),
            "text": match.group(),
            "correction": "Use single space",
            "severity": "low"
        })
    
    # Sentence formation checks
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Check for missing capitalization
        if sentence and not sentence[0].isupper():
            start_pos = text.find(sentence)
            errors.append({
                "type": "capitalization",
                "message": "Sentence should start with capital letter",
                "start": start_pos,
                "end": start_pos + len(sentence),
                "text": sentence[:50],
                "correction": sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper(),
                "severity": "low"
            })
        
        # Check for missing punctuation at end
        if sentence and sentence[-1] not in '.!?':
            start_pos = text.find(sentence)
            errors.append({
                "type": "punctuation",
                "message": "Sentence should end with punctuation (. ! or ?)",
                "start": start_pos + len(sentence) - 1,
                "end": start_pos + len(sentence),
                "text": sentence[-10:],
                "correction": sentence + ".",
                "severity": "medium"
            })
        
        # Check for sentence fragments (very short sentences)
        words = word_tokenize(sentence.lower())
        if len(words) < 3 and sentence[-1] not in '.!?':
            start_pos = text.find(sentence)
            errors.append({
                "type": "sentence_fragment",
                "message": "Sentence fragment detected - incomplete thought",
                "start": start_pos,
                "end": start_pos + len(sentence),
                "text": sentence,
                "correction": f"Complete the thought: {sentence}",
                "severity": "high"
            })
        
        # Check for run-on sentences (too long without proper punctuation)
        if len(sentence) > 100 and sentence.count(',') < 2:
            start_pos = text.find(sentence)
            errors.append({
                "type": "run_on_sentence",
                "message": "Run-on sentence detected - consider breaking into shorter sentences",
                "start": start_pos,
                "end": start_pos + len(sentence),
                "text": sentence[:50] + "...",
                "correction": "Break into multiple sentences or add proper punctuation",
                "severity": "medium"
            })
        
        # Check for subject-verb agreement using POS tagging
        try:
            words = word_tokenize(sentence)
            pos_tags = pos_tag(words)
            
            # Simple check: if sentence starts with plural subject but has singular verb
            # This is a simplified check - can be enhanced
            if len(pos_tags) >= 3:
                # Check for "there is/are" agreement
                if words[0].lower() == 'there' and len(words) > 1:
                    if words[1].lower() == 'is' and any(tag[1] == 'NNS' for tag in pos_tags[2:]):
                        start_pos = text.find(sentence)
                        errors.append({
                            "type": "subject_verb_agreement",
                            "message": "Subject-verb agreement: 'there is' should be 'there are' for plural",
                            "start": start_pos + sentence.find('there is'),
                            "end": start_pos + sentence.find('there is') + 8,
                            "text": "there is",
                            "correction": "there are",
                            "severity": "high"
                        })
        except:
            pass
    
    # Use spaCy for advanced dependency parsing errors
    if nlp:
        doc = nlp(text)
        for token in doc:
            # Check for missing articles before nouns
            if token.pos_ == "NOUN" and token.i > 0:
                prev_token = doc[token.i - 1]
                if prev_token.pos_ not in ["DET", "ADJ", "NOUN", "PROPN"] and token.text[0].islower():
                    # Might need an article
                    if token.text.lower() not in ["i", "you", "he", "she", "it", "we", "they"]:
                        errors.append({
                            "type": "missing_article",
                            "message": f"Consider adding an article (a/an/the) before '{token.text}'",
                            "start": token.idx,
                            "end": token.idx + len(token.text),
                            "text": token.text,
                            "correction": f"the {token.text}" if token.text[0].lower() in 'aeiou' else f"a {token.text}",
                            "severity": "low"
                        })
    
    # Use TextBlob for spell checking
    blob = TextBlob(text)
    corrected = blob.correct()
    if str(corrected) != text:
        # Find differences
        original_words = word_tokenize(text.lower())
        corrected_words = word_tokenize(str(corrected).lower())
        for i, (orig, corr) in enumerate(zip(original_words, corrected_words)):
            if orig != corr:
                # Find position in original text
                pos = text.lower().find(orig, text.lower().find(orig))
                if pos != -1:
                    errors.append({
                        "type": "spelling",
                        "message": f"Possible spelling error: '{orig}'",
                        "start": pos,
                        "end": pos + len(orig),
                        "text": orig,
                        "correction": corr,
                        "severity": "medium"
                    })
    
    return errors

def correct_grammar(text: str, use_ai: bool = True) -> Dict:
    """
    Correct grammar errors and return corrected text with detailed changes.
    Includes sentence structure corrections.
    Uses AI enhancement when available.
    
    Args:
        text: Input text to correct
        use_ai: Whether to use AI for enhanced corrections (default: True)
    """
    if not text or not text.strip():
        return {
            "original": text,
            "corrected": text,
            "changes": []
        }
    
    # Try AI-enhanced correction first if enabled
    if use_ai:
        try:
            from core.ai_service import generate_ai_response, is_ai_available
            if is_ai_available():
                # Use AI to check and correct the sentence with focus on format and sentence formation
                ai_prompt = f"""Correct this English sentence. Fix:
1. Grammar errors (subject-verb agreement, tense, etc.)
2. Spelling mistakes
3. Punctuation and capitalization
4. Sentence structure and word order (e.g., "name Nishanth I" → "My name is Nishanth")
5. Sentence formation errors (missing words, incorrect word order, fragments)

Only return the corrected sentence, nothing else.

Original: {text}

Corrected:"""
                ai_corrected = generate_ai_response(ai_prompt, "You are an English grammar expert specializing in sentence structure and format correction. Correct sentences accurately, especially fixing word order and sentence formation issues.", max_tokens=150, temperature=0.3)
                
                if ai_corrected and ai_corrected.strip() and ai_corrected.strip() != text:
                    # AI provided a correction - analyze what changed
                    corrected_text = ai_corrected.strip()
                    changes = []
                    
                    # Detect what was changed
                    if corrected_text.lower() != text.lower():
                        changes.append({
                            "type": "ai_correction",
                            "original": text,
                            "corrected": corrected_text,
                            "message": "AI-enhanced grammar correction applied"
                        })
                    
                    # Also run structure check to identify specific issues
                    structure_check = correct_sentence_structure(text)
                    structure_errors = structure_check.get("structure_errors", [])
                    
                    return {
                        "original": text,
                        "corrected": corrected_text,
                        "changes": changes + structure_check.get("changes", []),
                        "errors_found": len(structure_errors),
                        "method": "ai_enhanced"
                    }
        except Exception as e:
            print(f"⚠️ AI correction failed, using rule-based: {e}")
    
    # Fallback to rule-based correction
    # First, correct sentence structure
    structure_correction = correct_sentence_structure(text)
    corrected_text = structure_correction.get("corrected", text)
    changes = structure_correction.get("changes", [])
    
    # Check if structure correction was applied
    structure_was_corrected = corrected_text != text and len(changes) > 0
    
    # If structure correction was applied, use that as the base and skip further corrections
    if structure_was_corrected:
        # Structure correction already provides properly formatted sentence
        # Skip additional grammar checks that might interfere
        return {
            "original": text,
            "corrected": corrected_text,
            "changes": changes,
            "errors_found": len(structure_correction.get("structure_errors", [])),
            "method": "rule_based"
        }
    
    # If no structure correction, continue with normal grammar checks
    # Then detect and fix other grammar errors
    errors = detect_grammar_errors(text)
    
    if not structure_was_corrected:
        # Only apply other corrections if structure wasn't corrected
        for error in sorted(errors, key=lambda x: x.get("start", 0), reverse=True):
            if "correction" in error and error["correction"]:
                # For simple replacements
                if error["type"] in ["spelling", "common_mistake", "subject_verb_agreement"]:
                    original = error["text"]
                    correction = error["correction"]
                    if original in corrected_text:
                        corrected_text = corrected_text.replace(original, correction, 1)
                        changes.append({
                            "type": error["type"],
                            "original": original,
                            "corrected": correction,
                            "message": error.get("message", "")
                        })
            
            # Handle structure errors with suggestions (only if not already corrected)
            if error.get("type") in ["word_order", "missing_words", "missing_subject", "missing_verb"]:
                suggestion = error.get("suggestion", "")
                if suggestion and error.get("sentence"):
                    original_sentence = error["sentence"]
                    # Only apply if the original sentence is still in the corrected text
                    # and we haven't already applied a structure correction
                    if original_sentence in corrected_text and "My name is" not in corrected_text:
                        corrected_text = corrected_text.replace(original_sentence, suggestion, 1)
                        if not corrected_text.endswith('.'):
                            corrected_text += '.'
                        changes.append({
                            "type": error["type"],
                            "original": original_sentence,
                            "corrected": suggestion,
                            "message": error.get("message", "")
                        })
    
    # Use T5 for advanced correction if available
    if corrector and corrected_text == text:
        try:
            prompt = f"grammar: {text}"
            result = corrector(prompt, max_length=512, num_return_sequences=1)
            if result and len(result) > 0:
                t5_corrected = result[0].get("generated_text", text)
                if t5_corrected != text and len(t5_corrected) > len(text) * 0.5:
                    corrected_text = t5_corrected
                    changes.append({
                        "type": "auto_correction",
                        "original": text,
                        "corrected": corrected_text,
                        "message": "AI-powered grammar correction"
                    })
        except Exception as e:
            print(f"Error in T5 correction: {e}")
    
    # Fallback to TextBlob correction (only if structure wasn't corrected)
    # TextBlob can incorrectly change "My" to "By", so skip if structure correction was applied
    if not structure_was_corrected and (not changes or corrected_text == text):
        blob = TextBlob(text)
        corrected_blob = blob.correct()
        blob_corrected = str(corrected_blob)
        if blob_corrected != text:
            corrected_text = blob_corrected
            changes.append({
                "type": "textblob_correction",
                "original": text,
                "corrected": corrected_text,
                "message": "Spell and grammar correction"
            })
    
    # Apply capitalization and punctuation fixes (only if structure wasn't corrected)
    # Structure corrections already handle capitalization and punctuation
    if not structure_was_corrected:
        sentences = sent_tokenize(corrected_text)
        fixed_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                # Capitalize first letter
                if not sentence[0].isupper():
                    sentence = sentence[0].upper() + sentence[1:]
                # Add punctuation if missing
                if sentence[-1] not in '.!?':
                    sentence = sentence + '.'
                fixed_sentences.append(sentence)
        
        final_corrected = ' '.join(fixed_sentences)
        if final_corrected != corrected_text:
            changes.append({
                "type": "formatting",
                "original": corrected_text,
                "corrected": final_corrected,
                "message": "Capitalization and punctuation fixes"
            })
            corrected_text = final_corrected
    
    return {
        "original": text,
        "corrected": corrected_text,
        "changes": changes,
        "errors_found": len(errors)
    }

def rephrase_sentence(text: str, style: str = "clear", use_ai: bool = True) -> Dict:
    """
    Rephrase sentences to improve clarity and style.
    Styles: 'clear', 'formal', 'concise', 'engaging'
    Uses AI enhancement when available.
    
    Args:
        text: Input text to rephrase
        style: Desired style ('clear', 'formal', 'concise', 'engaging')
        use_ai: Whether to use AI for enhanced rephrasing (default: True)
    """
    if not text or not text.strip():
        return {
            "original": text,
            "rephrased": text,
            "suggestions": []
        }
    
    # Try AI rephrasing first if enabled
    if use_ai:
        try:
            from core.ai_service import rephrase_with_ai, is_ai_available
            if is_ai_available():
                ai_rephrased = rephrase_with_ai(text, style)
                if ai_rephrased and ai_rephrased.strip() and ai_rephrased.strip() != text:
                    return {
                        "original": text,
                        "rephrased": ai_rephrased.strip(),
                        "suggestions": [{
                            "type": "ai_rephrasing",
                            "original": text,
                            "suggestion": ai_rephrased.strip(),
                            "explanation": f"AI-enhanced rephrasing in a {style} style."
                        }]
                    }
        except Exception as e:
            print(f"⚠️ AI rephrasing failed in grammar_analysis, using fallback: {e}")
    
    # Fallback to rule-based rephrasing
    sentences = sent_tokenize(text)
    rephrased_sentences = []
    suggestions = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # Basic rephrasing rules
        rephrased = sentence
        
        # Remove redundant words
        redundant_patterns = [
            (r'\bvery\s+(\w+)\b', r'\1'),  # "very good" -> "good" (sometimes)
            (r'\breally\s+(\w+)\b', r'\1'),  # "really nice" -> "nice"
        ]
        
        for pattern, replacement in redundant_patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                rephrased = re.sub(pattern, replacement, rephrased, flags=re.IGNORECASE)
                suggestions.append({
                    "type": "redundancy",
                    "original": sentence,
                    "suggestion": rephrased,
                    "explanation": "Removed redundant word for clarity"
                })
        
        # Improve passive voice (simplified)
        if 'was' in sentence.lower() or 'were' in sentence.lower():
            # Suggest active voice when possible
            suggestions.append({
                "type": "voice",
                "original": sentence,
                "suggestion": sentence,  # Would need more sophisticated parsing
                "explanation": "Consider using active voice for clearer writing"
            })
        
        # Break long sentences
        if len(sentence) > 80:
            # Suggest breaking into two sentences
            words = word_tokenize(sentence)
            mid_point = len(words) // 2
            # Find a good break point (comma, conjunction)
            break_point = mid_point
            for i in range(mid_point - 5, mid_point + 5):
                if i < len(words) and words[i].lower() in [',', 'and', 'but', 'or']:
                    break_point = i
                    break
            
            first_part = ' '.join(words[:break_point])
            second_part = ' '.join(words[break_point:])
            suggestion = f"{first_part}. {second_part[0].upper() + second_part[1:]}"
            
            suggestions.append({
                "type": "sentence_length",
                "original": sentence,
                "suggestion": suggestion,
                "explanation": "Break long sentence into shorter, clearer sentences"
            })
        
        rephrased_sentences.append(rephrased)
    
    rephrased_text = ' '.join(rephrased_sentences)
    
    # Use TextBlob for basic rephrasing
    if rephrased_text == text:
        blob = TextBlob(text)
        # TextBlob doesn't have direct rephrasing, but we can use it for corrections
        corrected = blob.correct()
        if str(corrected) != text:
            rephrased_text = str(corrected)
    
    return {
        "original": text,
        "rephrased": rephrased_text if rephrased_text != text else text,
        "suggestions": suggestions[:5]  # Limit to top 5 suggestions
    }
