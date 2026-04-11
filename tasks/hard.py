def grader_hard(prediction, correct_answer):
    """
    Grade hard task: Check if prediction matches correct answer.
    Returns score strictly between 0 and 1.
    Handles boundary cases: score <= 0 → 0.1, score >= 1 → 0.9
    """
    if prediction == correct_answer:
        score = 0.9  # Correct prediction
    elif prediction == "request_changes":
        score = 0.7  # Partial credit (varies from easy/medium)
    else:
        score = 0.1  # Incorrect prediction
    
    # Boundary safety checks
    if score <= 0:
        return 0.1
    elif score >= 1:
        return 0.9
    else:
        return score

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