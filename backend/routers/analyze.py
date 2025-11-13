from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.user_model import User
from models.progress_model import Progress
from models.feedback_model import FeedbackLog
from core.auth import get_current_user_optional
from beanie import PydanticObjectId
from core.preprocessing import preprocess_text
from core.grammar_analysis import detect_grammar_errors, correct_grammar, rephrase_sentence
from core.lexical_semantic import calculate_lexical_diversity, suggest_synonyms, extract_keywords, analyze_semantic_coherence
from core.readability import calculate_readability
from core.tone_style import analyze_tone_and_style
from core.proficiency_model import predict_proficiency
from core.summarizer_qg import summarize_text, generate_questions
from core.explainable_ai import explain_correction, explain_proficiency_prediction

router = APIRouter(prefix="/analyze", tags=["analyze"])

class AnalyzeRequest(BaseModel):
    text: str
    user_id: Optional[int] = None

@router.post("/")
async def analyze_text(request: AnalyzeRequest, current_user: Optional[User] = Depends(get_current_user_optional)):
    """
    Comprehensive text analysis endpoint.
    Performs grammar, vocabulary, readability, tone, and proficiency analysis.
    """
    try:
        if not request.text or len(request.text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Text must be at least 10 characters long")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in analyze_text (initial check): {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")
    
    try:
        
        text = request.text.strip()
        user_id = str(current_user.id) if current_user else None
        
        # Preprocessing
        try:
            preprocessed = preprocess_text(text)
        except Exception as e:
            print(f"Error in preprocessing: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Preprocessing error: {str(e)}")
        
        # Grammar Analysis (with AI enhancement)
        try:
            grammar_errors = detect_grammar_errors(text)
            grammar_correction = correct_grammar(text, use_ai=True)  # Enable AI for grammar correction
        except Exception as e:
            print(f"Error in grammar analysis: {e}")
            import traceback
            traceback.print_exc()
            # Use fallback values
            grammar_errors = []
            grammar_correction = {"original": text, "corrected": text, "changes": [], "errors_found": 0}
        
        # Rephrasing suggestions (with AI enhancement)
        try:
            rephrasing = rephrase_sentence(text, style="clear", use_ai=True)  # Enable AI for rephrasing
        except Exception as e:
            print(f"Error in rephrasing: {e}")
            rephrasing = {
                "original": text,
                "rephrased": text,
                "suggestions": []
            }
        
        # Lexical & Semantic Analysis
        try:
            lexical_metrics = calculate_lexical_diversity(preprocessed.get("tokens", []))
            keywords = extract_keywords(text, top_n=10)
            coherence = analyze_semantic_coherence(text)
        except Exception as e:
            print(f"Error in lexical analysis: {e}")
            lexical_metrics = {"ttr": 0.5, "unique_words": 0, "total_words": 0}
            keywords = []
            coherence = {"coherence_score": 0.5, "topic_consistency": "medium"}
        
        # Readability Analysis
        try:
            readability = calculate_readability(text)
        except Exception as e:
            print(f"Error in readability analysis: {e}")
            readability = {
                "flesch_reading_ease": 50.0,
                "flesch_kincaid_grade": 8.0,
                "avg_sentence_length": 10.0
            }
        
        # Tone & Style Analysis
        try:
            tone_style = analyze_tone_and_style(text)
        except Exception as e:
            print(f"Error in tone analysis: {e}")
            tone_style = {
                "tone": "neutral",
                "sentiment": {"polarity": 0.0, "subjectivity": 0.5}
            }
        
        # Proficiency Prediction
        try:
            proficiency_features = {
                "grammar_errors": len(grammar_errors),
                "flesch_reading_ease": readability.get("flesch_reading_ease", 50.0),
                "ttr": lexical_metrics.get("ttr", 0.5),
                "avg_sentence_length": readability.get("avg_sentence_length", 10.0),
                "word_count": preprocessed.get("word_count", len(text.split()))
            }
            proficiency = predict_proficiency(proficiency_features)
            proficiency_explanation = explain_proficiency_prediction(proficiency, proficiency_features)
        except Exception as e:
            print(f"Error in proficiency prediction: {e}")
            proficiency = {"cefr_level": "B1", "confidence": 0.5}
            proficiency_explanation = "Unable to predict proficiency level."
        
        # Generate corrections with explanations
        corrections_with_explanations = []
        for error in grammar_errors[:10]:  # Limit to top 10 errors
            # Safely get error text
            error_text = ""
            if "start" in error and "end" in error:
                start = error.get("start", 0)
                end = error.get("end", len(text))
                if start < len(text) and end <= len(text):
                    error_text = text[start:end]
            elif "text" in error:
                error_text = error["text"]
            elif "sentence" in error:
                error_text = error["sentence"]
            
            # Use correction from error if available, otherwise use error_text
            correction_text = error.get("correction", error_text)
            error_type = error.get("type", "general")
            
            try:
                explanation = explain_correction(
                    error_text,
                    correction_text,
                    error_type
                )
                corrections_with_explanations.append({
                    **error,
                    "explanation": explanation.get("explanation", ""),
                    "rule": explanation.get("rule", ""),
                    "suggested_correction": correction_text if "correction" in error else None
                })
            except Exception as e:
                # Fallback if explanation fails
                corrections_with_explanations.append({
                    **error,
                    "explanation": f"Error type: {error_type}",
                    "rule": "Grammar rule",
                    "suggested_correction": correction_text if "correction" in error else None
                })
        
        # Save to database if user is authenticated
        if user_id and current_user:
            try:
                # Save feedback log
                feedback_log = FeedbackLog(
                    user_id=PydanticObjectId(user_id),
                    text=text,
                    corrections=corrections_with_explanations,
                    suggestions=keywords
                )
                await feedback_log.insert()
                
                # Update or create progress
                today = datetime.utcnow().date()
                today_start = datetime.combine(today, datetime.min.time())
                
                progress = await Progress.find_one(
                    Progress.user_id == PydanticObjectId(user_id),
                    Progress.date >= today_start
                )
                
                if not progress:
                    progress = Progress(
                        user_id=PydanticObjectId(user_id),
                        grammar_errors=len(grammar_errors),
                        readability=readability["flesch_reading_ease"],
                        sentiment=tone_style["sentiment"]["polarity"],
                        cefr_level=proficiency["cefr_level"],
                        lexical_diversity=lexical_metrics["ttr"]
                    )
                    await progress.insert()
                else:
                    progress.grammar_errors = len(grammar_errors)
                    progress.readability = readability["flesch_reading_ease"]
                    progress.sentiment = tone_style["sentiment"]["polarity"]
                    progress.cefr_level = proficiency["cefr_level"]
                    progress.lexical_diversity = lexical_metrics["ttr"]
                    await progress.save()
            except Exception as e:
                print(f"Error saving to database: {e}")
                import traceback
                traceback.print_exc()
        
        try:
            return {
            "grammar": {
                "errors": corrections_with_explanations,
                "error_count": len(grammar_errors),
                "corrected_text": grammar_correction["corrected"],
                "changes": grammar_correction["changes"],
                "errors_found": grammar_correction.get("errors_found", 0)
            },
            "rephrasing": {
                "original": rephrasing["original"],
                "rephrased": rephrasing["rephrased"],
                "suggestions": rephrasing["suggestions"]
            },
            "vocabulary": {
                "lexical_diversity": lexical_metrics,
                "keywords": keywords,
                "suggestions": [suggest_synonyms(word["word"], text) for word in keywords[:3]]
            },
            "readability": readability,
            "tone_style": tone_style,
            "proficiency": {
                **proficiency,
                "explanation": proficiency_explanation
            },
            "coherence": coherence,
            "preprocessing": {
                "word_count": preprocessed.get("word_count", 0),
                "sentence_count": preprocessed.get("sentence_count", 0),
                "entities": preprocessed.get("entities", [])[:5]
            }
        }
        except Exception as e:
            print(f"Error building response: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Error building response: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in analyze_text: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/summarize")
async def summarize(request: AnalyzeRequest):
    """Summarize text endpoint."""
    if not request.text:
        raise HTTPException(status_code=400, detail="Text is required")
    
    summary = summarize_text(request.text)
    return summary

@router.post("/questions")
async def generate_quiz(request: AnalyzeRequest):
    """Generate comprehension questions from text."""
    if not request.text:
        raise HTTPException(status_code=400, detail="Text is required")
    
    questions = generate_questions(request.text, num_questions=5)
    return {"questions": questions}
