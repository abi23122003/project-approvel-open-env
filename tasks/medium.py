def grader_medium(prediction, correct_answer):
    """
    Grade medium task: Check if prediction matches correct answer.
    Returns score strictly between 0 and 1.
    Handles boundary cases: score <= 0 → 0.1, score >= 1 → 0.9
    """
    if prediction == correct_answer:
        score = 0.9  # Correct prediction
    elif prediction == "request_changes":
        score = 0.6  # Partial credit (varies from easy)
    else:
        score = 0.1  # Incorrect prediction
    
    # Boundary safety checks
    if score <= 0:
        return 0.1
    elif score >= 1:
        return 0.9
    else:
        return score

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