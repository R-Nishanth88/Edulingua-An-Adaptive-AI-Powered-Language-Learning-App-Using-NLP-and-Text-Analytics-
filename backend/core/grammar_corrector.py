"""
Advanced Grammar Correction using Transformer Models.
Uses T5-based grammar correction models for accurate fixes.
"""
from typing import Dict, Optional
import re

# Try to import transformers
try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    AutoTokenizer = None
    AutoModelForSeq2SeqLM = None
    pipeline = None

# Global model instances
grammar_tokenizer = None
grammar_model = None
grammar_pipeline = None

def load_grammar_model():
    """Lazy load grammar correction model."""
    global grammar_tokenizer, grammar_model, grammar_pipeline
    
    if not TRANSFORMERS_AVAILABLE:
        return False
    
    if grammar_pipeline is not None:
        return True
    
    try:
        # Try using pipeline first (simpler)
        grammar_pipeline = pipeline(
            "text2text-generation",
            model="vennify/t5-base-grammar-correction",
            device=-1  # CPU
        )
        print("✅ Grammar correction model loaded (pipeline)")
        return True
    except Exception as e:
        print(f"⚠️ Could not load grammar correction model: {e}")
        try:
            # Fallback to manual loading
            grammar_tokenizer = AutoTokenizer.from_pretrained("vennify/t5-base-grammar-correction")
            grammar_model = AutoModelForSeq2SeqLM.from_pretrained("vennify/t5-base-grammar-correction")
            print("✅ Grammar correction model loaded (manual)")
            return True
        except Exception as e2:
            print(f"⚠️ Could not load grammar correction model (fallback): {e2}")
            return False

def correct_text(text: str, use_model: bool = True) -> Dict[str, str]:
    """
    Correct grammar errors in text using T5 model.
    
    Args:
        text: Input text with potential grammar errors
        use_model: Whether to use transformer model (fallback to rule-based if False)
    
    Returns:
        Dictionary with original and corrected text
    """
    if not text or not text.strip():
        return {
            "original": text,
            "corrected": text,
            "method": "none"
        }
    
    original_text = text.strip()
    
    # Try to use transformer model
    if use_model and TRANSFORMERS_AVAILABLE:
        if load_grammar_model():
            try:
                if grammar_pipeline:
                    # Use pipeline
                    input_text = f"grammar: {original_text}"
                    result = grammar_pipeline(
                        input_text,
                        max_length=256,
                        num_beams=5,
                        early_stopping=True,
                        num_return_sequences=1
                    )
                    if result and len(result) > 0:
                        corrected = result[0].get("generated_text", original_text)
                        if corrected and corrected != original_text:
                            return {
                                "original": original_text,
                                "corrected": corrected.strip(),
                                "method": "t5_model"
                            }
                elif grammar_tokenizer and grammar_model:
                    # Use manual tokenization
                    input_text = f"grammar: {original_text}"
                    inputs = grammar_tokenizer.encode(
                        input_text,
                        return_tensors="pt",
                        max_length=256,
                        truncation=True
                    )
                    outputs = grammar_model.generate(
                        inputs,
                        max_length=256,
                        num_beams=5,
                        early_stopping=True
                    )
                    corrected = grammar_tokenizer.decode(outputs[0], skip_special_tokens=True)
                    if corrected and corrected != original_text:
                        return {
                            "original": original_text,
                            "corrected": corrected.strip(),
                            "method": "t5_model"
                        }
            except Exception as e:
                print(f"⚠️ Error in grammar correction model: {e}")
                # Fallback to rule-based
    
    # Fallback to rule-based correction (using existing sentence structure module)
    try:
        from .sentence_structure import correct_sentence_structure
        result = correct_sentence_structure(original_text)
        corrected = result.get("corrected", original_text)
        
        # Ensure proper formatting
        if corrected:
            corrected = corrected.strip()
            if corrected and not corrected[0].isupper():
                corrected = corrected[0].upper() + corrected[1:]
            if corrected and corrected[-1] not in '.!?':
                corrected = corrected + '.'
        
        if corrected and corrected != original_text:
            return {
                "original": original_text,
                "corrected": corrected,
                "method": "rule_based"
            }
    except Exception as e:
        print(f"⚠️ Error in rule-based correction: {e}")
        import traceback
        traceback.print_exc()
    
    # If no correction found, return original
    return {
        "original": original_text,
        "corrected": original_text,
        "method": "none"
    }

def correct_batch(texts: list[str]) -> list[Dict[str, str]]:
    """
    Correct multiple texts in batch.
    
    Args:
        texts: List of texts to correct
    
    Returns:
        List of correction results
    """
    return [correct_text(text) for text in texts]

