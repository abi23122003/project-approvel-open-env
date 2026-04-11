from tasks.easy import grader_easy
from tasks.medium import grader_medium
from tasks.hard import grader_hard

def grade(predicted, correct):
    """
    Main grader function: Validates predictions against correct answers.
    Returns score strictly between 0 and 1.
    Handles boundary cases: score <= 0 → 0.1, score >= 1 → 0.9
    """
    if predicted == correct:
        score = 0.9  # Correct decision
    elif predicted == "request_changes":
        score = 0.5  # Partial credit for request_changes
    else:
        score = 0.1  # Incorrect decision
    
    # Boundary safety checks
    if score <= 0:
        return 0.1
    elif score >= 1:
        return 0.9
    else:
        return score

# Task graders - all with boundary safety
graders = {
    "easy": grader_easy,
    "medium": grader_medium,
    "hard": grader_hard
}