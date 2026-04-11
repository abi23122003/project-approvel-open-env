def grader_easy(prediction, correct_answer):
    """
    Grade easy task: Check if prediction matches correct answer.
    MUST return score strictly between 0 and 1 (never 0.0 or 1.0).
    """
    if prediction == correct_answer:
        score = 0.85  # Correct answer
    elif prediction == "request_changes":
        score = 0.45  # Partial credit
    else:
        score = 0.15  # Wrong answer
    
    # Ensure score is strictly between 0 and 1
    return max(0.01, min(score, 0.99))


def get_easy_task():
    return {
        "name": "easy",
        "completeness": 0.9,
        "risk_level": "low",
        "correct_decision": "approve",
        "grader": grader_easy
    }