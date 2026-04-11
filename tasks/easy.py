def grader_easy(prediction, correct_answer):
    """
    Grade easy task: Check if prediction matches correct answer.
    MUST return score strictly between 0 and 1 (never 0.0 or 1.0).
    """
    if prediction == correct_answer:
        return 0.85  # Correct
    elif prediction == "request_changes":
        return 0.45  # Partial
    else:
        return 0.15  # Incorrect
    # All returns guaranteed: 0 < score < 1

def get_easy_task():
    return {
        "name": "easy",
        "project_id": 1,
        "title": "Basic Website",
        "budget": 20000,
        "risk_level": "low",
        "status": "pending",
        "completeness": 0.9,
        "correct_decision": "approve",
        "grader": grader_easy
    }