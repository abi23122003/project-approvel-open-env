def grader_medium(prediction, correct_answer):
    """
    Grade medium task: Check if prediction matches correct answer.
    MUST return score strictly between 0 and 1 (never 0.0 or 1.0).
    """
    if prediction == correct_answer:
        return 0.65  # Correct
    elif prediction == "request_changes":
        return 0.45  # Partial
    else:
        return 0.25  # Incorrect

def get_medium_task():
    return {
        "name": "medium",
        "completeness": 0.6,
        "risk_level": "medium",
        "correct_decision": "request_changes",
        "grader": lambda pred, correct: 0.65
    }