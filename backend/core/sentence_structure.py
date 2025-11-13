"""
Advanced sentence structure analysis and correction.
Detects word order issues, missing words, and structural problems.
"""
import re
from typing import List, Dict, Tuple, Optional
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag

# Try to import spaCy
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    spacy = None

nlp = None
if SPACY_AVAILABLE:
    try:
        nlp = spacy.load("en_core_web_sm")
    except (OSError, IOError):
        nlp = None

def analyze_sentence_structure(text: str) -> Dict:
    """
    Analyze sentence structure and detect structural errors.
    """
    errors = []
    corrections = []
    
    if not text or not text.strip():
        return {"errors": errors, "corrections": corrections}
    
    sentences = sent_tokenize(text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # Use spaCy for dependency parsing if available
        if nlp:
            doc = nlp(sentence)
            structure_errors = detect_structure_errors_spacy(doc, sentence)
            errors.extend(structure_errors)
        else:
            # Fallback to rule-based analysis
            structure_errors = detect_structure_errors_rulebased(sentence)
            errors.extend(structure_errors)
        
        # Generate corrections
        if errors:
            correction = generate_structure_correction(sentence, errors)
            if correction and correction != sentence:
                corrections.append({
                    "original": sentence,
                    "corrected": correction,
                    "errors": [e["type"] for e in errors if e.get("sentence") == sentence]
                })
    
    return {
        "errors": errors,
        "corrections": corrections,
        "has_structure_errors": len(errors) > 0
    }

def detect_structure_errors_spacy(doc, sentence: str) -> List[Dict]:
    """
    Use spaCy dependency parsing to detect structural errors.
    """
    errors = []
    
    # Check for missing subject
    has_subject = False
    has_verb = False
    has_object = False
    
    for token in doc:
        # Check for subject (nsubj, nsubjpass)
        if token.dep_ in ["nsubj", "nsubjpass"]:
            has_subject = True
        # Check for verb (ROOT with verb POS)
        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            has_verb = True
        # Check for object (dobj, pobj)
        if token.dep_ in ["dobj", "pobj"]:
            has_object = True
    
    # Missing subject error
    if not has_subject and has_verb:
        # Check if it's imperative (commands don't need subjects)
        if not any(token.text.lower() in ["please", "let", "make"] for token in doc):
            errors.append({
                "type": "missing_subject",
                "message": "Sentence is missing a subject",
                "sentence": sentence,
                "severity": "high",
                "suggestion": "Add a subject (I, You, He, She, It, We, They, or a noun)"
            })
    
    # Missing verb error
    if has_subject and not has_verb:
        errors.append({
            "type": "missing_verb",
            "message": "Sentence is missing a verb",
            "sentence": sentence,
            "severity": "high",
            "suggestion": "Add a verb to complete the sentence"
        })
    
    # Check for word order issues
    word_order_errors = detect_word_order_errors(doc, sentence)
    errors.extend(word_order_errors)
    
    # Check for missing articles
    article_errors = detect_missing_articles(doc, sentence)
    errors.extend(article_errors)
    
    # Check for missing prepositions
    preposition_errors = detect_missing_prepositions(doc, sentence)
    errors.extend(preposition_errors)
    
    return errors

def detect_structure_errors_rulebased(sentence: str) -> List[Dict]:
    """
    Rule-based structure error detection (fallback when spaCy not available).
    """
    errors = []
    words = word_tokenize(sentence.lower())
    
    # Very short sentences might be fragments
    if len(words) < 3:
        errors.append({
            "type": "sentence_fragment",
            "message": "Sentence appears incomplete",
            "sentence": sentence,
            "severity": "high",
            "suggestion": "Complete the sentence with a subject and verb"
        })
    
    # Check for common patterns that indicate structure issues
    # Pattern: "i [name] name" -> should be "my name is [name]"
    if re.match(r'^i\s+\w+\s+name', sentence.lower()):
        errors.append({
            "type": "word_order",
            "message": "Incorrect sentence structure. Use 'My name is [name]' format",
            "sentence": sentence,
            "severity": "high",
            "suggestion": "My name is [name]"
        })
    
    # Pattern: "[name] name" -> should be "My name is [name]"
    if re.match(r'^\w+\s+name$', sentence.lower()) and len(words) == 2:
        name = words[0]
        errors.append({
            "type": "missing_words",
            "message": "Missing words. Use 'My name is [name]' format",
            "sentence": sentence,
            "severity": "high",
            "suggestion": f"My name is {name.capitalize()}"
        })
    
    # Pattern: "name [name]" -> should be "My name is [name]"
    if re.match(r'^name\s+\w+$', sentence.lower()) and len(words) == 2:
        name = words[1]
        errors.append({
            "type": "word_order",
            "message": "Incorrect word order. Use 'My name is [name]' format",
            "sentence": sentence,
            "severity": "high",
            "suggestion": f"My name is {name.capitalize()}"
        })
    
    # Pattern: "name [name] I" or "[name] name I" -> should be "My name is [name]"
    if re.match(r'^name\s+\w+\s+i$', sentence.lower(), re.IGNORECASE) or \
       re.match(r'^\w+\s+name\s+i$', sentence.lower(), re.IGNORECASE):
        # Extract name
        parts = sentence.lower().split()
        name = None
        for part in parts:
            if part not in ["name", "i"]:
                name = part
                break
        if name:
            errors.append({
                "type": "word_order",
                "message": "Incorrect word order. Use 'My name is [name]' format",
                "sentence": sentence,
                "severity": "high",
                "suggestion": f"My name is {name.capitalize()}"
            })
    
    # Pattern: "[name] am i" -> should be "My name is [name]" or "I am [name]"
    if re.match(r'^\w+\s+am\s+i$', sentence.lower(), re.IGNORECASE):
        parts = sentence.lower().split()
        name = parts[0] if parts else None
        if name and name not in ["i", "am"]:
            errors.append({
                "type": "word_order",
                "message": "Incorrect word order. Use 'My name is [name]' or 'I am [name]' format",
                "sentence": sentence,
                "severity": "high",
                "suggestion": f"My name is {name.capitalize()}"
            })
    
    # Check for missing "is/am/are" after subject
    if words[0] in ["i", "you", "he", "she", "it", "we", "they"] and len(words) > 1:
        if words[1] not in ["am", "is", "are", "was", "were", "have", "has", "had", "will", "can", "should", "would", "could"]:
            # Check if second word is a noun (might need a verb)
            if len(words) > 2:
                errors.append({
                    "type": "missing_verb",
                    "message": "Missing verb after subject",
                    "sentence": sentence,
                    "severity": "medium",
                    "suggestion": f"Add a verb like 'is', 'am', 'are', 'have', etc."
                })
    
    # Check for "I am [noun]" -> should be "I am a [noun]"
    if re.match(r'^i\s+am\s+(\w+)$', sentence.lower()):
        match = re.match(r'^i\s+am\s+(\w+)$', sentence.lower(), re.IGNORECASE)
        if match:
            noun = match.group(1)
            # Check if it's a common noun (not a proper noun)
            if noun[0].islower() and noun not in ["ok", "fine", "good", "well", "here", "there"]:
                errors.append({
                    "type": "missing_article",
                    "message": "Missing article 'a' or 'an' before the noun",
                    "sentence": sentence,
                    "severity": "medium",
                    "suggestion": f"I am a {noun}" if noun[0].lower() not in "aeiou" else f"I am an {noun}"
                })
    
    # Check for "[subject] is [noun]" without article
    if re.match(r'^(the|a|an|this|that|my|your|his|her|its|our|their)\s+\w+\s+is\s+(\w+)$', sentence.lower()):
        match = re.match(r'^(the|a|an|this|that|my|your|his|her|its|our|their)\s+\w+\s+is\s+(\w+)$', sentence.lower(), re.IGNORECASE)
        if match:
            noun = match.group(2)
            # If noun is lowercase and not a proper noun, might need article or preposition
            if noun[0].islower() and noun not in ["good", "bad", "fine", "ok", "here", "there", "mine", "yours"]:
                errors.append({
                    "type": "missing_article_or_preposition",
                    "message": "Consider adding 'a/an' or a preposition like 'on', 'in', 'at'",
                    "sentence": sentence,
                    "severity": "low",
                    "suggestion": f"{sentence} a {noun}" if noun[0].lower() not in "aeiou" else f"{sentence} an {noun}"
                })
    
    # Check for "I like [verb]" -> should be "I like to [verb]" or "I like [verb]ing"
    # Only check if not already matched by two-word pattern
    if not re.match(r'^i\s+like\s+(\w+)\s+(\w+)$', sentence.lower()):
        if re.match(r'^i\s+like\s+(\w+)$', sentence.lower()):
            match = re.match(r'^i\s+like\s+(\w+)$', sentence.lower(), re.IGNORECASE)
            if match:
                verb = match.group(1)
                # Check if it's likely a verb (not a noun)
                if verb not in ["it", "this", "that", "you", "him", "her", "them", "music", "food"]:
                    errors.append({
                        "type": "missing_infinitive",
                        "message": "Missing 'to' before verb or use '-ing' form",
                        "sentence": sentence,
                        "severity": "medium",
                        "suggestion": f"I like to {verb}"  # or f"I like {verb}ing"
                    })
    
    # Check for patterns like "I [verb] [verb] [noun]" -> should be "I [verb] to [verb] [noun]"
    # Common verbs that need "to" before another verb: like, want, need, try, start, begin, etc.
    infinitive_verbs = ["like", "want", "need", "try", "start", "begin", "love", "hate", "prefer", "decide", "plan", "hope", "expect"]
    for infin_verb in infinitive_verbs:
        pattern = rf'^i\s+{infin_verb}\s+(\w+)(?:\s+(\w+))?$'
        if re.match(pattern, sentence.lower()):
            match = re.match(pattern, sentence.lower(), re.IGNORECASE)
            if match:
                first_word = match.group(1)
                second_word = match.group(2) if match.lastindex >= 2 else None
                # Common verbs that need "to"
                common_verbs = ["play", "read", "write", "go", "come", "see", "watch", "eat", "drink", "buy", "sell", "make", "do", "take", "give", "get", "have", "learn", "study", "work"]
                # If first word is likely a verb
                if first_word.lower() in common_verbs or (first_word not in ["the", "a", "an", "my", "your", "this", "that", "it", "music", "food", "books"]):
                    if second_word:
                        errors.append({
                            "type": "missing_infinitive",
                            "message": f"Missing 'to' before verb after '{infin_verb}'",
                            "sentence": sentence,
                            "severity": "medium",
                            "suggestion": f"I {infin_verb} to {first_word} {second_word}"
                        })
                    else:
                        errors.append({
                            "type": "missing_infinitive",
                            "message": f"Missing 'to' before verb after '{infin_verb}'",
                            "sentence": sentence,
                            "severity": "medium",
                            "suggestion": f"I {infin_verb} to {first_word}"
                        })
                    break  # Only match one pattern
    
    return errors

def detect_word_order_errors(doc, sentence: str) -> List[Dict]:
    """
    Detect word order issues using dependency parsing.
    """
    errors = []
    
    # Check for common word order patterns
    words = [token.text for token in doc]
    pos_tags = [token.pos_ for token in doc]
    
    # Pattern: Subject-Verb-Object should be in order
    # If we have NOUN VERB NOUN but they're not in S-V-O order
    for i, token in enumerate(doc):
        # Check for "I [name] name" pattern
        if (token.text.lower() == "i" and i + 2 < len(doc) and 
            doc[i+2].text.lower() == "name"):
            errors.append({
                "type": "word_order",
                "message": "Incorrect word order. Use 'My name is [name]'",
                "sentence": sentence,
                "start": token.idx,
                "end": doc[i+2].idx + len(doc[i+2].text),
                "text": f"{token.text} {doc[i+1].text} {doc[i+2].text}",
                "severity": "high",
                "suggestion": f"My name is {doc[i+1].text}"
            })
    
    return errors

def detect_missing_articles(doc, sentence: str) -> List[Dict]:
    """
    Detect missing articles (a, an, the) before nouns.
    """
    errors = []
    
    for i, token in enumerate(doc):
        # Check if noun needs an article
        if token.pos_ == "NOUN" and not token.text[0].isupper():  # Not a proper noun
            # Check if previous token is not an article, determiner, or adjective
            if i > 0:
                prev_token = doc[i-1]
                if prev_token.pos_ not in ["DET", "ADJ"] and prev_token.text.lower() not in ["a", "an", "the", "my", "your", "his", "her", "its", "our", "their"]:
                    # Check if it's the start of a noun phrase
                    if i == 0 or (i > 0 and doc[i-1].pos_ not in ["VERB", "ADP"]):
                        errors.append({
                            "type": "missing_article",
                            "message": f"Consider adding an article (a/an/the) before '{token.text}'",
                            "sentence": sentence,
                            "start": token.idx,
                            "end": token.idx + len(token.text),
                            "text": token.text,
                            "severity": "low",
                            "suggestion": f"the {token.text}" if token.text[0].lower() not in "aeiou" else f"an {token.text}"
                        })
    
    return errors

def detect_missing_prepositions(doc, sentence: str) -> List[Dict]:
    """
    Detect missing prepositions in common patterns.
    """
    errors = []
    
    # Common patterns that need prepositions
    patterns = [
        (r'\b(interested|good|bad)\s+(\w+)\b', "in"),
        (r'\b(depends|rely)\s+(\w+)\b', "on"),
        (r'\b(listen|look)\s+(\w+)\b', "to/at"),
    ]
    
    for pattern, prep in patterns:
        matches = re.finditer(pattern, sentence.lower())
        for match in matches:
            word_after = match.group(2)
            # Check if preposition is missing
            if not re.search(rf'\b{prep.split("/")[0]}\s+{word_after}', sentence.lower()):
                errors.append({
                    "type": "missing_preposition",
                    "message": f"Missing preposition '{prep}' after '{match.group(1)}'",
                    "sentence": sentence,
                    "start": match.start(),
                    "end": match.end(),
                    "text": match.group(0),
                    "severity": "medium",
                    "suggestion": f"{match.group(1)} {prep.split('/')[0]} {word_after}"
                })
    
    return errors

def generate_structure_correction(sentence: str, errors: List[Dict]) -> str:
    """
    Generate corrected sentence based on structure errors.
    """
    corrected = sentence
    
    # Sort errors by position (reverse order for safe replacement)
    sentence_errors = [e for e in errors if e.get("sentence") == sentence]
    sentence_errors.sort(key=lambda x: x.get("start", 0), reverse=True)
    
    for error in sentence_errors:
        error_type = error.get("type")
        suggestion = error.get("suggestion", "")
        
        if error_type == "word_order":
            # Handle "i [name] name" -> "My name is [name]"
            if re.match(r'^i\s+(\w+)\s+name', sentence.lower()):
                match = re.match(r'^i\s+(\w+)\s+name', sentence.lower(), re.IGNORECASE)
                if match:
                    name = match.group(1)
                    corrected = f"My name is {name.capitalize()}."
                    break
            # Handle "name [name] I" -> "My name is [name]"
            elif re.match(r'^name\s+\w+\s+i$', sentence.lower(), re.IGNORECASE):
                parts = sentence.lower().split()
                name = None
                for part in parts:
                    if part not in ["name", "i"]:
                        name = part
                        break
                if name:
                    corrected = f"My name is {name.capitalize()}."
                    break
            # Use suggestion if available
            elif suggestion and "My name is" in suggestion:
                corrected = suggestion
                if not corrected.endswith('.'):
                    corrected += '.'
                break
        
        elif error_type == "missing_words":
            # Handle "[name] name" -> "My name is [name]"
            if re.match(r'^(\w+)\s+name$', sentence.lower()):
                match = re.match(r'^(\w+)\s+name$', sentence.lower(), re.IGNORECASE)
                if match:
                    name = match.group(1)
                    corrected = f"My name is {name.capitalize()}."
                    break
        elif error_type == "word_order":
            # Handle "[name] am i" -> "My name is [name]"
            if re.match(r'^(\w+)\s+am\s+i$', sentence.lower(), re.IGNORECASE):
                match = re.match(r'^(\w+)\s+am\s+i$', sentence.lower(), re.IGNORECASE)
                if match:
                    name = match.group(1)
                    if name.lower() not in ["i", "am"]:
                        corrected = f"My name is {name.capitalize()}."
                        break
            # Handle "name [name]" -> "My name is [name]"
            elif re.match(r'^name\s+(\w+)$', sentence.lower()):
                match = re.match(r'^name\s+(\w+)$', sentence.lower(), re.IGNORECASE)
                if match:
                    name = match.group(1)
                    corrected = f"My name is {name.capitalize()}."
                    break
        
        elif error_type == "missing_subject":
            # Try to infer subject from context
            if suggestion:
                # Add suggested subject
                if corrected[0].islower():
                    corrected = suggestion.split()[0].capitalize() + " " + corrected
                else:
                    corrected = suggestion + " " + corrected
        
        elif error_type == "missing_verb":
            # Add common verbs based on context
            if "name" in sentence.lower():
                if "my" in sentence.lower() or "i" in sentence.lower():
                    corrected = sentence.replace("name", "name is")
                else:
                    corrected = "My name is " + sentence.split()[-1] if sentence.split() else sentence
        
        elif error_type == "missing_article":
            # Add article before noun
            if "i am" in sentence.lower():
                match = re.match(r'^i\s+am\s+(\w+)$', sentence.lower(), re.IGNORECASE)
                if match:
                    noun = match.group(1)
                    article = "a" if noun[0].lower() not in "aeiou" else "an"
                    corrected = f"I am {article} {noun.capitalize()}."
                    break
        
        elif error_type == "missing_article" and error.get("start") is not None:
            # Add article before the word
            start = error["start"]
            text = error["text"]
            suggestion_text = error.get("suggestion", f"the {text}")
            if start < len(corrected):
                corrected = corrected[:start] + suggestion_text + " " + corrected[start:]
        
        elif error_type == "missing_infinitive":
            # Handle missing "to" before verbs (e.g., "i like play" -> "i like to play")
            if suggestion:
                corrected = suggestion
                break
            # Try to add "to" before the verb
            infinitive_verbs = ["like", "want", "need", "try", "start", "begin", "love", "hate", "prefer", "decide", "plan", "hope", "expect"]
            for infin_verb in infinitive_verbs:
                pattern2 = rf'^i\s+{infin_verb}\s+(\w+)\s+(\w+)$'
                match2 = re.match(pattern2, sentence.lower(), re.IGNORECASE)
                if match2:
                    first_word = match2.group(1)
                    second_word = match2.group(2)
                    corrected = f"I {infin_verb} to {first_word} {second_word.capitalize()}."
                    break
                pattern1 = rf'^i\s+{infin_verb}\s+(\w+)$'
                match1 = re.match(pattern1, sentence.lower(), re.IGNORECASE)
                if match1:
                    first_word = match1.group(1)
                    corrected = f"I {infin_verb} to {first_word.capitalize()}."
                    break
    
    # Use TextBlob for additional corrections
    if corrected == sentence:
        blob = TextBlob(sentence)
        corrected_blob = blob.correct()
        if str(corrected_blob) != sentence:
            corrected = str(corrected_blob)
    
    # Ensure proper capitalization and punctuation
    if corrected:
        corrected = corrected.strip()
        if corrected and not corrected[0].isupper():
            corrected = corrected[0].upper() + corrected[1:]
        if corrected and corrected[-1] not in '.!?':
            corrected = corrected + '.'
    
    return corrected

def correct_sentence_structure(text: str) -> Dict:
    """
    Main function to correct sentence structure issues.
    """
    if not text or not text.strip():
        return {
            "original": text,
            "corrected": text,
            "changes": []
        }
    
    analysis = analyze_sentence_structure(text)
    errors = analysis["errors"]
    corrections = analysis["corrections"]
    
    # Generate final corrected text
    corrected_text = text
    changes = []
    
    # Apply corrections
    for correction in corrections:
        if correction["original"] in corrected_text:
            corrected_text = corrected_text.replace(
                correction["original"],
                correction["corrected"],
                1
            )
            changes.append({
                "type": "structure_correction",
                "original": correction["original"],
                "corrected": correction["corrected"],
                "errors_fixed": correction["errors"]
            })
    
    # If no corrections found, try intelligent correction
    if corrected_text == text and errors:
        # Prioritize specific error types - infinitive errors first
        infinitive_errors = [e for e in errors if e.get("type") == "missing_infinitive"]
        word_order_errors = [e for e in errors if e.get("type") in ["word_order", "missing_words"]]
        article_errors = [e for e in errors if e.get("type") == "missing_article"]
        other_errors = [e for e in errors if e.get("severity") in ["high", "medium"] and e.get("type") not in ["missing_infinitive", "word_order", "missing_words", "missing_article"]]
        
        # Try to fix in priority order
        error = None
        if infinitive_errors:
            error = infinitive_errors[0]
        elif word_order_errors:
            error = word_order_errors[0]
        elif article_errors:
            error = article_errors[0]
        elif other_errors:
            error = other_errors[0]
        
        if error:
            suggestion = error.get("suggestion", "")
            error_type = error.get("type", "")
            
            # Apply corrections based on error type
            if error_type == "missing_infinitive":
                # Try to match various patterns
                infinitive_verbs = ["like", "want", "need", "try", "start", "begin", "love", "hate", "prefer", "decide", "plan", "hope", "expect"]
                matched = False
                for infin_verb in infinitive_verbs:
                    # Try two-word pattern first
                    pattern2 = rf'^i\s+{infin_verb}\s+(\w+)\s+(\w+)$'
                    match2 = re.match(pattern2, text.lower(), re.IGNORECASE)
                    if match2:
                        first_word = match2.group(1)
                        second_word = match2.group(2)
                        corrected_text = f"I {infin_verb} to {first_word} {second_word.capitalize()}."
                        changes.append({
                            "type": "structure_correction",
                            "original": text,
                            "corrected": corrected_text,
                            "errors_fixed": ["missing_infinitive"]
                        })
                        matched = True
                        break
                    # Try single-word pattern
                    pattern1 = rf'^i\s+{infin_verb}\s+(\w+)$'
                    match1 = re.match(pattern1, text.lower(), re.IGNORECASE)
                    if match1:
                        first_word = match1.group(1)
                        corrected_text = f"I {infin_verb} to {first_word.capitalize()}."
                        changes.append({
                            "type": "structure_correction",
                            "original": text,
                            "corrected": corrected_text,
                            "errors_fixed": ["missing_infinitive"]
                        })
                        matched = True
                        break
                
                # If no pattern matched, use suggestion
                if not matched and suggestion:
                    corrected_text = suggestion
                    if not corrected_text.endswith('.'):
                        corrected_text += '.'
                    changes.append({
                        "type": "structure_correction",
                        "original": text,
                        "corrected": corrected_text,
                        "errors_fixed": ["missing_infinitive"]
                    })
            elif suggestion:
                # For patterns like "i nishanth name"
                if re.match(r'^i\s+\w+\s+name', text.lower()):
                    match = re.match(r'^i\s+(\w+)\s+name', text.lower(), re.IGNORECASE)
                    if match:
                        name = match.group(1)
                        corrected_text = f"My name is {name.capitalize()}."
                        changes.append({
                            "type": "structure_correction",
                            "original": text,
                            "corrected": corrected_text,
                            "errors_fixed": ["word_order", "missing_words"]
                        })
                # For patterns like "nishanth name"
                elif re.match(r'^\w+\s+name$', text.lower()):
                    match = re.match(r'^(\w+)\s+name$', text.lower(), re.IGNORECASE)
                    if match:
                        name = match.group(1)
                        corrected_text = f"My name is {name.capitalize()}."
                        changes.append({
                            "type": "structure_correction",
                            "original": text,
                            "corrected": corrected_text,
                            "errors_fixed": ["missing_words", "word_order"]
                        })
                # For pattern "[name] am i" -> "My name is [name]"
                elif re.match(r'^(\w+)\s+am\s+i$', text.lower(), re.IGNORECASE):
                    match = re.match(r'^(\w+)\s+am\s+i$', text.lower(), re.IGNORECASE)
                    if match:
                        name = match.group(1)
                        if name.lower() not in ["i", "am"]:
                            corrected_text = f"My name is {name.capitalize()}."
                            changes.append({
                                "type": "structure_correction",
                                "original": text,
                                "corrected": corrected_text,
                                "errors_fixed": ["word_order"]
                            })
                # For patterns like "name nishanth i" or "nishanth name i"
                elif re.match(r'^name\s+\w+\s+i$', text.lower(), re.IGNORECASE) or \
                     re.match(r'^\w+\s+name\s+i$', text.lower(), re.IGNORECASE):
                    parts = text.lower().split()
                    name = None
                    for part in parts:
                        if part not in ["name", "i"]:
                            name = part
                            break
                    if name:
                        corrected_text = f"My name is {name.capitalize()}."
                        changes.append({
                            "type": "structure_correction",
                            "original": text,
                            "corrected": corrected_text,
                            "errors_fixed": ["word_order", "missing_words"]
                        })
                # Use suggestion directly if it contains the corrected format
                elif suggestion and "My name is" in suggestion:
                    corrected_text = suggestion
                    if not corrected_text.endswith('.'):
                        corrected_text += '.'
                    changes.append({
                        "type": "structure_correction",
                        "original": text,
                        "corrected": corrected_text,
                        "errors_fixed": [error_type]
                    })
                # For "I am [noun]" -> "I am a [noun]"
                elif error_type == "missing_article" and "i am" in text.lower():
                    match = re.match(r'^i\s+am\s+(\w+)$', text.lower(), re.IGNORECASE)
                    if match:
                        noun = match.group(1)
                        article = "a" if noun[0].lower() not in "aeiou" else "an"
                        corrected_text = f"I am {article} {noun.capitalize()}."
                        changes.append({
                            "type": "structure_correction",
                            "original": text,
                            "corrected": corrected_text,
                            "errors_fixed": ["missing_article"]
                        })
                # For "I like [verb]" -> "I like to [verb]"
                elif error_type == "missing_infinitive" and "i like" in text.lower():
                    # Try two-word pattern first
                    match = re.match(r'^i\s+like\s+(\w+)\s+(\w+)$', text.lower(), re.IGNORECASE)
                    if match:
                        first_word = match.group(1)
                        second_word = match.group(2)
                        corrected_text = f"I like to {first_word} {second_word.capitalize()}."
                    else:
                        # Single word pattern
                        match = re.match(r'^i\s+like\s+(\w+)$', text.lower(), re.IGNORECASE)
                        if match:
                            verb = match.group(1)
                            corrected_text = f"I like to {verb.capitalize()}."
                    if corrected_text != text:
                        changes.append({
                            "type": "structure_correction",
                            "original": text,
                            "corrected": corrected_text,
                            "errors_fixed": ["missing_infinitive"]
                        })
                # Use the suggestion directly if available
                elif suggestion and suggestion != text:
                    corrected_text = suggestion
                    changes.append({
                        "type": "structure_correction",
                        "original": text,
                        "corrected": corrected_text,
                        "errors_fixed": [error_type]
                    })
    
    return {
        "original": text,
        "corrected": corrected_text,
        "changes": changes,
        "errors_found": len(errors),
        "structure_errors": errors
    }

