def grader_easy(prediction, correct_answer):
    """
    Grade easy task: Check if prediction matches correct answer.
    MUST return score strictly between 0 and 1 (never 0.0 or 1.0).
    """
    if prediction == correct_answer:
        return 0.6  # Correct
    elif prediction == "request_changes":
        return 0.4  # Partial
    else:
        return 0.2  # Incorrect

def get_easy_task():
    return {
        "name": "easy",
        "completeness": 0.9,
        "risk_level": "low",
        "correct_decision": "approve",
        "grader": lambda pred, correct: 0.6
    }