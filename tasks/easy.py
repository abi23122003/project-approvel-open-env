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
    scenarios = [
        {
            "name": "easy",
            "project_id": random.randint(1000, 9999),
            "title": "Community Library Renovation",
            "budget": 50000,
            "risk_level": "low",
            "status": "pending",
            "completeness": 0.95,
            "correct_decision": "approve",
            "grader": grader_easy
        },
        {
            "name": "easy",
            "project_id": random.randint(1000, 9999),
            "title": "School Playground Equipment Upgrade",
            "budget": 35000,
            "risk_level": "low",
            "status": "pending",
            "completeness": 0.90,
            "correct_decision": "approve",
            "grader": grader_easy
        },
        {
            "name": "easy",
            "project_id": random.randint(1000, 9999),
            "title": "Office HVAC System Replacement",
            "budget": 28000,
            "risk_level": "low",
            "status": "pending",
            "completeness": 0.88,
            "correct_decision": "approve",
            "grader": grader_easy
        },
        {
            "name": "easy",
            "project_id": random.randint(1000, 9999),
            "title": "Employee Training Program",
            "budget": 15000,
            "risk_level": "low",
            "status": "pending",
            "completeness": 0.92,
            "correct_decision": "approve",
            "grader": grader_easy
        }
    ]
    return random.choice(scenarios)