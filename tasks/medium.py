def grader_medium(prediction, correct_answer):
    """
    Grade medium task: Check if prediction matches correct answer.
    MUST return score strictly between 0 and 1 (never 0.0 or 1.0).
    """
    if prediction == correct_answer:
        return 0.78  # Correct
    elif prediction == "request_changes":
        return 0.55  # Partial
    else:
        return 0.22  # Incorrect
    # All returns guaranteed: 0 < score < 1

def get_medium_task():
    return {
        "name": "medium",
        "project_id": 2,
        "title": "Mobile App",
        "budget": 50000,
        "risk_level": "medium",
        "status": "pending",
        "completeness": 0.6,
        "correct_decision": "request_changes",
        "grader": grader_medium
    }