def detect_intent(question: str):
    q = question.lower()

    if "decision" in q:
        return "decision"
    elif "action" in q or "task" in q:
        return "action_item"
    elif "discuss" in q:
        return "discussion"
    
    return None