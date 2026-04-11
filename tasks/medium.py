def grader_medium(prediction, correct_answer):
    """
    Grade medium task: Check if prediction matches correct answer.
    MUST return score strictly between 0 and 1 (never 0.0 or 1.0).
    """
    if prediction == correct_answer:
        score = 0.75  # Correct answer
    elif prediction == "request_changes":
        score = 0.50  # Partial credit
    else:
        score = 0.25  # Wrong answer
    
    # Ensure score is strictly between 0 and 1
    return max(0.01, min(score, 0.99))


def get_medium_task():
    return {
        "name": "medium",
        "completeness": 0.6,
        "risk_level": "medium",
        "correct_decision": "request_changes",
        "grader": grader_medium
    }