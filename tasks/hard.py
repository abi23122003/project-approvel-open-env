def grader_hard(prediction, correct_answer):
    """
    Grade hard task: Check if prediction matches correct answer.
    MUST return score strictly between 0 and 1 (never 0.0 or 1.0).
    """
    if prediction == correct_answer:
        return 0.82  # Correct
    elif prediction == "request_changes":
        return 0.65  # Partial
    else:
        return 0.28  # Incorrect
    # All returns guaranteed: 0 < score < 1

def get_hard_task():
    return {
        "name": "hard",
        "project_id": 3,
        "title": "AI System",
        "budget": 150000,
        "risk_level": "high",
        "status": "pending",
        "completeness": 0.8,
        "correct_decision": "reject",
        "grader": grader_hard
    }