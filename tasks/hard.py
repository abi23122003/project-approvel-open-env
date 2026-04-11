import random

def grader_hard(prediction, correct_answer):
    if prediction == correct_answer:
        score = 0.80
    elif prediction == "request_changes":
        score = 0.55
    else:
        score = 0.30
    return max(0.01, min(score, 0.99))

def get_hard_task():
    return {
        "project_id": random.randint(1000, 9999),
        "title": "Nuclear Waste Processing Plant",
        "budget": 9500000,
        "risk_level": "high",
        "status": "pending",
        "completeness": 0.3,
        "correct_decision": "reject",
        "grader": grader_hard
    }