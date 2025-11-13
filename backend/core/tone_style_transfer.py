"""
Tone and Style Transfer Module
Rephrase text into different tones: Formal, Friendly, Academic, Creative, Concise
"""
from typing import Dict, List, Optional
from core.ai_service import generate_ai_response, is_ai_available, rephrase_with_ai

# Tone definitions
TONE_STYLES = {
    "formal": {
        "description": "Professional, respectful, and structured language",
        "characteristics": [
            "Uses complete sentences",
            "Avoids contractions",
            "Professional vocabulary",
            "Structured and clear"
        ],
        "example": "I would like to request your assistance"  # vs "I'd like your help"
    },
    "friendly": {
        "description": "Warm, approachable, and conversational",
        "characteristics": [
            "Uses contractions naturally",
            "Conversational tone",
            "Friendly expressions",
            "Personal pronouns"
        ],
        "example": "I'd love to help you out!"  # vs "I would be pleased to assist"
    },
    "academic": {
        "description": "Scholarly, precise, and evidence-based",
        "characteristics": [
            "Technical vocabulary",
            "Formal structure",
            "Citations and references",
            "Objective tone"
        ],
        "example": "The research indicates that..."  # vs "Studies show..."
    },
    "creative": {
        "description": "Expressive, vivid, and engaging",
        "characteristics": [
            "Vivid descriptions",
            "Figurative language",
            "Varied sentence structure",
            "Engaging narrative"
        ],
        "example": "The sun painted the sky in brilliant hues of orange and pink"
    },
    "concise": {
        "description": "Brief, direct, and to the point",
        "characteristics": [
            "Short sentences",
            "No redundancy",
            "Direct language",
            "Essential information only"
        ],
        "example": "Meeting at 3 PM. Bring notes."  # vs "We will have a meeting at 3 PM. Please bring your notes."
    },
    "casual": {
        "description": "Relaxed, informal, and everyday language",
        "characteristics": [
            "Colloquial expressions",
            "Informal vocabulary",
            "Relaxed structure",
            "Everyday language"
        ],
        "example": "Hey, what's up? Want to grab coffee?"
    }
}

def transfer_tone(text: str, target_tone: str, use_ai: bool = True) -> Dict:
    """
    Rephrase text into a different tone/style.
    
    Args:
        text: Input text to rephrase
        target_tone: Target tone (formal, friendly, academic, creative, concise, casual)
        use_ai: Whether to use AI for tone transfer
    
    Returns:
        Dictionary with rephrased text and tone analysis
    """
    if not text or not text.strip():
        return {
            "original": text,
            "rephrased": text,
            "target_tone": target_tone,
            "success": False
        }
    
    target_tone = target_tone.lower()
    
    if target_tone not in TONE_STYLES:
        return {
            "original": text,
            "rephrased": text,
            "target_tone": target_tone,
            "success": False,
            "error": f"Unknown tone: {target_tone}. Available: {list(TONE_STYLES.keys())}"
        }
    
    tone_info = TONE_STYLES[target_tone]
    
    # Use AI for tone transfer
    if use_ai and is_ai_available():
        try:
            system_prompt = f"""You are a professional writing style expert. Rephrase text to match the {target_tone} tone.
            
Target Tone: {target_tone.upper()}
Description: {tone_info['description']}
Characteristics: {', '.join(tone_info['characteristics'])}

Maintain the original meaning while adapting the tone."""
            
            prompt = f"""Rephrase the following text in a {target_tone} tone:

Original: {text}

Rephrased ({target_tone} tone):"""
            
            ai_rephrased = generate_ai_response(
                prompt,
                system_prompt,
                max_tokens=300,
                temperature=0.7
            )
            
            if ai_rephrased and ai_rephrased.strip():
                return {
                    "original": text,
                    "rephrased": ai_rephrased.strip(),
                    "target_tone": target_tone,
                    "tone_info": tone_info,
                    "success": True,
                    "method": "ai_enhanced"
                }
        except Exception as e:
            print(f"⚠️ AI tone transfer failed: {e}")
    
    # Fallback: Use rephrase_with_ai from ai_service
    try:
        rephrased = rephrase_with_ai(text, style=target_tone)
        if rephrased and rephrased != text:
            return {
                "original": text,
                "rephrased": rephrased,
                "target_tone": target_tone,
                "tone_info": tone_info,
                "success": True,
                "method": "ai_fallback"
            }
    except Exception as e:
        print(f"⚠️ Fallback tone transfer failed: {e}")
    
    # Final fallback: return original
    return {
        "original": text,
        "rephrased": text,
        "target_tone": target_tone,
        "tone_info": tone_info,
        "success": False,
        "error": "Tone transfer unavailable"
    }

def get_available_tones() -> List[Dict]:
    """Get list of available tone styles."""
    return [
        {
            "name": tone,
            "description": info["description"],
            "characteristics": info["characteristics"],
            "example": info["example"]
        }
        for tone, info in TONE_STYLES.items()
    ]

def detect_current_tone(text: str) -> Dict:
    """
    Detect the current tone/style of the text.
    
    Returns:
        Dictionary with detected tone and confidence
    """
    if not text or not text.strip():
        return {
            "detected_tone": "neutral",
            "confidence": 0.0
        }
    
    if is_ai_available():
        try:
            prompt = f"""Analyze the tone and style of this text. Choose from: formal, friendly, academic, creative, concise, casual, or neutral.

Text: {text}

Respond with only the tone name (e.g., "formal" or "friendly")."""
            
            detected = generate_ai_response(
                prompt,
                "You are a writing style analyzer. Identify the tone of text accurately.",
                max_tokens=20,
                temperature=0.3
            )
            
            if detected:
                detected_tone = detected.strip().lower()
                # Validate detected tone
                if detected_tone in TONE_STYLES or detected_tone == "neutral":
                    return {
                        "detected_tone": detected_tone,
                        "confidence": 0.8,
                        "method": "ai_detection"
                    }
        except Exception as e:
            print(f"⚠️ Tone detection failed: {e}")
    
    # Fallback: simple rule-based detection
    text_lower = text.lower()
    
    # Check for formal indicators
    if any(word in text_lower for word in ["would like", "please", "respectfully", "sincerely"]):
        return {"detected_tone": "formal", "confidence": 0.6, "method": "rule_based"}
    
    # Check for casual indicators
    if any(word in text_lower for word in ["hey", "what's up", "gonna", "wanna"]):
        return {"detected_tone": "casual", "confidence": 0.6, "method": "rule_based"}
    
    # Check for academic indicators
    if any(word in text_lower for word in ["research", "study", "analysis", "evidence", "indicates"]):
        return {"detected_tone": "academic", "confidence": 0.6, "method": "rule_based"}
    
    return {"detected_tone": "neutral", "confidence": 0.4, "method": "rule_based"}

