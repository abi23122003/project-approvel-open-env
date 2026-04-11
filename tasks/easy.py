import random

def grader_easy(prediction, correct_answer):
    if prediction == correct_answer:
        score = 0.85
    elif prediction == "request_changes":
        score = 0.45
    else:
        score = 0.15
    return max(0.01, min(score, 0.99))

def get_easy_task():
    return {
        "name": "easy",
        "project_id": random.randint(1000, 9999),
        "title": "Community Library Renovation",
        "budget": 50000,
        "risk_level": "low",
        "status": "pending",
        "completeness": 0.9,
        "correct_decision": "approve",
        "grader": grader_easy
    }