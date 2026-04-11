def grader_hard(prediction, correct_answer):
    """
    Grade hard task: Check if prediction matches correct answer.
    MUST return score strictly between 0 and 1 (never 0.0 or 1.0).
    """
    if prediction == correct_answer:
        score = 0.80  # Correct answer
    elif prediction == "request_changes":
        score = 0.55  # Partial credit
    else:
        score = 0.30  # Wrong answer
    
    # Ensure score is strictly between 0 and 1
    return max(0.01, min(score, 0.99))


def get_hard_task():
    return {
        "name": "hard",
        "completeness": 0.3,
        "risk_level": "high",
        "correct_decision": "reject",
        "grader": grader_hard
    }