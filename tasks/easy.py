def grader_easy(prediction, correct_answer):
    """
    Grade easy task: Check if prediction matches correct answer.
    Returns score strictly between 0 and 1.
    """
    if prediction == correct_answer:
        return 0.9  # Correct prediction
    elif prediction == "request_changes":
        return 0.5  # Partial credit
    else:
        return 0.1  # Incorrect prediction

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