def supervisor_review(action, expected):
    penalty = 0.0
    notes = []

    reasoning = (action.reasoning or "").strip().lower()
    decision = action.decision.strip().lower()

    if len(reasoning.split()) < 5:
        penalty -= 0.15
        notes.append("reasoning too short")

    if expected["policy"].lower() not in reasoning:
        penalty -= 0.1
        notes.append("missing policy mention")

    if decision not in {"allow", "flag", "remove", "escalate"}:
        penalty -= 0.25
        notes.append("invalid decision")

    return penalty, notes