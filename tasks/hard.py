def grader_hard(prediction, correct_answer):
    """
    Grade hard task: Check if prediction matches correct answer.
    MUST return score strictly between 0 and 1 (never 0.0 or 1.0).
    """
    if prediction == correct_answer:
        return 0.7  # Correct
    elif prediction == "request_changes":
        return 0.5  # Partial
    else:
        return 0.3  # Incorrect

def get_hard_task():
    return {
        "name": "hard",
        "completeness": 0.3,
        "risk_level": "high",
        "correct_decision": "reject",
        "grader": lambda pred, correct: 0.7
    }