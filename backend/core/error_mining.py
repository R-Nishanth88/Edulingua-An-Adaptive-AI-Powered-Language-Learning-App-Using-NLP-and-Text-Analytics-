from typing import List, Dict
from collections import Counter
from core.grammar_analysis import detect_grammar_errors

def mine_common_errors(feedback_logs: List[Dict]) -> Dict:
    """
    Analyze feedback logs to identify common error patterns.
    """
    if not feedback_logs:
        return {
            "common_errors": [],
            "error_frequency": {},
            "trends": {}
        }
    
    all_errors = []
    error_types = []
    
    for log in feedback_logs:
        corrections = log.get("corrections", [])
        for correction in corrections:
            error_type = correction.get("type", "unknown")
            error_types.append(error_type)
            all_errors.append(correction)
    
    # Count error frequencies
    error_freq = Counter(error_types)
    
    # Get top 10 most common errors
    common_errors = []
    for error_type, count in error_freq.most_common(10):
        common_errors.append({
            "type": error_type,
            "frequency": count,
            "percentage": round((count / len(error_types) * 100), 2) if error_types else 0
        })
    
    return {
        "common_errors": common_errors,
        "error_frequency": dict(error_freq),
        "total_errors": len(error_types),
        "trends": {
            "most_common": error_freq.most_common(1)[0][0] if error_freq else None,
            "error_rate": len(error_types) / len(feedback_logs) if feedback_logs else 0
        }
    }
