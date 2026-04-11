import random

def grader_medium(prediction, correct_answer):
    if prediction == correct_answer:
        score = 0.75
    elif prediction == "request_changes":
        score = 0.50
    else:
        score = 0.25
    return max(0.01, min(score, 0.99))

def get_medium_task():
    scenarios = [
        {
            "name": "medium",
            "project_id": random.randint(1000, 9999),
            "title": "City Park Smart Lighting System",
            "budget": 120000,
            "risk_level": "medium",
            "status": "pending",
            "completeness": 0.60,
            "correct_decision": "request_changes",
            "grader": grader_medium
        },
        {
            "name": "medium",
            "project_id": random.randint(1000, 9999),
            "title": "Hospital Records Digitization",
            "budget": 200000,
            "risk_level": "medium",
            "status": "pending",
            "completeness": 0.55,
            "correct_decision": "request_changes",
            "grader": grader_medium
        },
        {
            "name": "medium",
            "project_id": random.randint(1000, 9999),
            "title": "Public Transport Mobile App",
            "budget": 85000,
            "risk_level": "medium",
            "status": "pending",
            "completeness": 0.62,
            "correct_decision": "request_changes",
            "grader": grader_medium
        },
        {
            "name": "medium",
            "project_id": random.randint(1000, 9999),
            "title": "Warehouse Inventory Automation",
            "budget": 175000,
            "risk_level": "medium",
            "status": "pending",
            "completeness": 0.50,
            "correct_decision": "request_changes",
            "grader": grader_medium
        }
    ]
    return random.choice(scenarios)