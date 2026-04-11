def grader_hard(prediction, correct_answer):
    """
    Grade hard task: Check if prediction matches correct answer.
    Returns score strictly between 0 and 1.
    """
    if prediction == correct_answer:
        return 0.9  # Correct prediction
    elif prediction == "request_changes":
        return 0.5  # Partial credit
    else:
        return 0.1  # Incorrect prediction

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