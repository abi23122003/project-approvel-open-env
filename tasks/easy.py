def grader_easy(prediction, correct_answer):
    """
    Grade easy task: Check if prediction matches correct answer.
    Returns score strictly between 0 and 1.
    Handles boundary cases: score <= 0 → 0.1, score >= 1 → 0.9
    """
    if prediction == correct_answer:
        score = 0.9  # Correct prediction
    elif prediction == "request_changes":
        score = 0.5  # Partial credit
    else:
        score = 0.1  # Incorrect prediction
    
    # Boundary safety checks
    if score <= 0:
        return 0.1
    elif score >= 1:
        return 0.9
    else:
        return score

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