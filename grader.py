def grade(predicted, correct):
    if predicted == correct:
        return 1.0
    elif predicted == "request_changes":
        return 0.5
    return 0.0