"""
Text Rephrasing Engine using Pegasus and other models.
Generates multiple fluent variants of corrected text.
"""
from typing import List, Dict, Optional

# Try to import transformers
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    pipeline = None

# Global model instances
rephrase_pipeline = None
pegasus_tokenizer = None
pegasus_model = None

def load_rephrase_model():
    """Lazy load rephrasing model."""
    global rephrase_pipeline, pegasus_tokenizer, pegasus_model
    
    if not TRANSFORMERS_AVAILABLE:
        return False
    
    if rephrase_pipeline is not None:
        return True
    
    try:
        # Try Pegasus paraphrase model
        rephrase_pipeline = pipeline(
            "text2text-generation",
            model="tuner007/pegasus_paraphrase",
            device=-1  # CPU
        )
        print("✅ Rephrasing model loaded (Pegasus)")
        return True
    except Exception as e:
        print(f"⚠️ Could not load Pegasus model: {e}")
        try:
            # Fallback to T5 for paraphrasing
            rephrase_pipeline = pipeline(
                "text2text-generation",
                model="t5-base",
                device=-1
            )
            print("✅ Rephrasing model loaded (T5 fallback)")
            return True
        except Exception as e2:
            print(f"⚠️ Could not load rephrasing model: {e2}")
            return False

def rephrase_text(text: str, num_variants: int = 3, style: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Generate rephrased variants of text.
    Uses AI enhancement when available.
    
    Args:
        text: Input text to rephrase
        num_variants: Number of variants to generate (default: 3)
        style: Style preference ("formal", "concise", "fluent", None for mixed)
    
    Returns:
        List of rephrased variants with style labels
    """
    if not text or not text.strip():
        return []
    
    text = text.strip()
    variants = []
    
    # Try AI rephrasing first
    try:
        from core.ai_service import rephrase_with_ai, is_ai_available
        if is_ai_available() and style:
            ai_rephrased = rephrase_with_ai(text, style)
            if ai_rephrased and ai_rephrased != text:
                variants.append({
                    "text": ai_rephrased,
                    "style": style,
                    "rank": 1
                })
    except Exception as e:
        print(f"⚠️ AI rephrasing failed, using fallback: {e}")
    
    # Try to use transformer model
    if TRANSFORMERS_AVAILABLE and load_rephrase_model():
        try:
            if rephrase_pipeline:
                # Generate variants
                if "pegasus" in str(rephrase_pipeline.model.config.name_or_path).lower():
                    # Pegasus-specific prompt
                    prompt = text
                else:
                    # T5 prompt
                    prompt = f"paraphrase: {text}"
                
                results = rephrase_pipeline(
                    prompt,
                    max_length=256,
                    num_beams=10,
                    num_return_sequences=min(num_variants, 5),
                    early_stopping=True
                )
                
                for i, result in enumerate(results):
                    if isinstance(result, dict):
                        generated = result.get("generated_text", "").strip()
                    else:
                        generated = str(result).strip()
                    
                    if generated and generated != text and len(generated) > 5:
                        # Determine style (simplified)
                        style_label = determine_style(generated, style)
                        variants.append({
                            "text": generated,
                            "style": style_label,
                            "rank": i + 1
                        })
        except Exception as e:
            print(f"⚠️ Error in rephrasing model: {e}")
    
    # Fallback to rule-based rephrasing
    if len(variants) < num_variants:
        rule_based = generate_rule_based_variants(text, num_variants - len(variants), style)
        variants.extend(rule_based)
    
    # Remove duplicates and limit
    seen = set()
    unique_variants = []
    for v in variants:
        text_key = v["text"].lower()
        if text_key not in seen and text_key != text.lower():
            seen.add(text_key)
            unique_variants.append(v)
            if len(unique_variants) >= num_variants:
                break
    
    return unique_variants

def determine_style(text: str, preferred_style: Optional[str] = None) -> str:
    """
    Determine the style of rephrased text.
    """
    if preferred_style:
        return preferred_style
    
    # Simple heuristics
    if len(text.split()) < 8:
        return "concise"
    elif any(word in text.lower() for word in ["furthermore", "moreover", "therefore", "consequently"]):
        return "formal"
    else:
        return "fluent"

def generate_rule_based_variants(text: str, num: int, style: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Generate rule-based rephrasing variants as fallback.
    """
    variants = []
    
    # Basic rephrasing patterns
    if "my name is" in text.lower():
        name_match = text.lower().replace("my name is", "").strip().rstrip(".")
        if name_match:
            variants.append({
                "text": f"I am {name_match.capitalize()}.",
                "style": "concise",
                "rank": 1
            })
            variants.append({
                "text": f"I'm {name_match.capitalize()}.",
                "style": "casual",
                "rank": 2
            })
    
    # Add more rule-based patterns as needed
    if len(variants) < num and "i like to" in text.lower():
        # Rephrase "I like to" patterns
        rest = text.lower().replace("i like to", "").strip().rstrip(".")
        if rest:
            variants.append({
                "text": f"I enjoy {rest}.",
                "style": "fluent",
                "rank": 1
            })
    
    return variants[:num]

def rephrase_with_style(text: str, style: str, num_variants: int = 2) -> List[str]:
    """
    Generate rephrased variants in a specific style.
    
    Args:
        text: Input text
        style: "formal", "concise", "fluent", "casual"
        num_variants: Number of variants
    
    Returns:
        List of rephrased texts
    """
    variants = rephrase_text(text, num_variants, style)
    return [v["text"] for v in variants if v.get("style") == style]

