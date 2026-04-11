def grader_medium(prediction, correct_answer):
    """
    Grade medium task: Check if prediction matches correct answer.
    Returns score strictly between 0 and 1.
    """
    if prediction == correct_answer:
        return 0.9  # Correct prediction
    elif prediction == "request_changes":
        return 0.5  # Partial credit
    else:
        return 0.1  # Incorrect prediction

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