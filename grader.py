from tasks.easy import grader_easy
from tasks.medium import grader_medium
from tasks.hard import grader_hard

def grade(predicted, correct):
    """
    Main grader function: Validates predictions against correct answers.
    Returns score strictly between 0 and 1.
    """
    if predicted == correct:
        return 0.9  # Correct decision
    elif predicted == "request_changes":
        return 0.5  # Partial credit for request_changes
    else:
        return 0.1  # Incorrect decision

# Task graders
graders = {
    "easy": grader_easy,
    "medium": grader_medium,
    "hard": grader_hard
}