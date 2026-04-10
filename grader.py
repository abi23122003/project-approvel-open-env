def grade(predicted, correct):
    if predicted == correct:
        return 0.9  # Changed from 1.0 - must be strictly between 0 and 1
    elif predicted == "request_changes":
        return 0.5
    return 0.1  # Changed from 0.0 - must be strictly between 0 and 1