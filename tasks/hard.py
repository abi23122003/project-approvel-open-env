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
    scenarios = [
        {
            "project_id": random.randint(1000, 9999),
            "title": "AI-Powered Medical Diagnosis System",
            "budget": 480000,
            "risk_level": "high",
            "status": "pending",
            "completeness": 0.72,
            "correct_decision": "request_changes",
            "grader": grader_hard
        },
        {
            "project_id": random.randint(1000, 9999),
            "title": "Smart City Traffic Optimization",
            "budget": 950000,
            "risk_level": "high",
            "status": "pending",
            "completeness": 0.65,
            "correct_decision": "request_changes",
            "grader": grader_hard
        },
        {
            "project_id": random.randint(1000, 9999),
            "title": "Autonomous Drone Delivery Network",
            "budget": 2100000,
            "risk_level": "high",
            "status": "pending",
            "completeness": 0.45,
            "correct_decision": "reject",
            "grader": grader_hard
        },
        {
            "project_id": random.randint(1000, 9999),
            "title": "Blockchain Supply Chain Tracker",
            "budget": 310000,
            "risk_level": "high",
            "status": "pending",
            "completeness": 0.58,
            "correct_decision": "request_changes",
            "grader": grader_hard
        }
    ]
    return random.choice(scenarios)