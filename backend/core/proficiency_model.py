from typing import Dict
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle
import os

# Simple proficiency classifier
# In production, this would be trained on a dataset
class ProficiencyClassifier:
    def __init__(self):
        self.model = None
        self.cefr_levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize a simple rule-based classifier (can be replaced with trained ML model)"""
        # For now, we'll use rule-based classification
        # In production, train on labeled data
        self.model = "rule_based"
    
    def predict(self, features: Dict) -> Dict:
        """
        Predict CEFR level based on text features.
        Features should include: grammar_errors, readability, lexical_diversity, etc.
        """
        grammar_errors = features.get("grammar_errors", 0)
        flesch_score = features.get("flesch_reading_ease", 50)
        ttr = features.get("ttr", 0.5)
        avg_sentence_length = features.get("avg_sentence_length", 10)
        word_count = features.get("word_count", 0)
        
        # Rule-based classification
        score = 0
        
        # Grammar errors (fewer is better)
        if grammar_errors == 0:
            score += 20
        elif grammar_errors < 3:
            score += 15
        elif grammar_errors < 5:
            score += 10
        elif grammar_errors < 10:
            score += 5
        
        # Readability (higher Flesch is easier, but we want appropriate complexity)
        # For advanced learners, lower Flesch (more complex) is better
        if 30 <= flesch_score <= 50:
            score += 20  # Complex text (C1-C2)
        elif 50 < flesch_score <= 70:
            score += 15  # Intermediate (B1-B2)
        elif flesch_score > 70:
            score += 10  # Simple (A1-A2)
        
        # Lexical diversity (higher TTR is better)
        if ttr > 0.7:
            score += 20
        elif ttr > 0.6:
            score += 15
        elif ttr > 0.5:
            score += 10
        elif ttr > 0.4:
            score += 5
        
        # Sentence complexity
        if 15 <= avg_sentence_length <= 25:
            score += 15
        elif avg_sentence_length > 25:
            score += 10
        else:
            score += 5
        
        # Word count (more words = more practice)
        if word_count > 200:
            score += 10
        elif word_count > 100:
            score += 5
        
        # Map score to CEFR level
        if score >= 80:
            level = "C2"
        elif score >= 70:
            level = "C1"
        elif score >= 60:
            level = "B2"
        elif score >= 50:
            level = "B1"
        elif score >= 40:
            level = "A2"
        else:
            level = "A1"
        
        confidence = min(score / 100, 1.0)
        
        return {
            "cefr_level": level,
            "confidence": round(confidence, 3),
            "score": score,
            "explanation": self._get_explanation(level, features)
        }
    
    def _get_explanation(self, level: str, features: Dict) -> str:
        """Generate explanation for the predicted level"""
        explanations = {
            "A1": "Beginner level. Focus on basic vocabulary and simple sentence structures.",
            "A2": "Elementary level. You're building foundational grammar and vocabulary.",
            "B1": "Intermediate level. Good grasp of grammar, expanding vocabulary range.",
            "B2": "Upper-intermediate level. Strong command of language with some complexity.",
            "C1": "Advanced level. Fluent and accurate with sophisticated language use.",
            "C2": "Proficient level. Near-native fluency and mastery of English."
        }
        
        base_explanation = explanations.get(level, "Unknown level")
        
        # Add specific feedback
        grammar_errors = features.get("grammar_errors", 0)
        if grammar_errors > 5:
            base_explanation += " Consider focusing on grammar accuracy."
        
        ttr = features.get("ttr", 0.5)
        if ttr < 0.5:
            base_explanation += " Try using more varied vocabulary."
        
        return base_explanation

# Global classifier instance
classifier = ProficiencyClassifier()

def predict_proficiency(text_features: Dict) -> Dict:
    """
    Predict user proficiency level based on text analysis features.
    """
    return classifier.predict(text_features)
