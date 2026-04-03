def grade_action(action, expected):
    decision_score = 0.0
    reasoning_score = 0.0
    policy_score = 0.0
    rewrite_score = 0.0

    decision = action.decision.strip().lower()
    reasoning = (action.reasoning or "").strip().lower()
    rewrite = (action.rewrite or "").strip()

    if decision == expected["decision"]:
        decision_score = 0.4

    keywords = expected.get("keywords", [])
    if keywords:
        hits = sum(1 for kw in keywords if kw.lower() in reasoning)
        reasoning_score = 0.3 * (hits / len(keywords))

    if expected.get("policy", "").lower() in reasoning:
        policy_score = 0.2

    if rewrite:
        rewrite_score = 0.1

    raw_score = decision_score + reasoning_score + policy_score + rewrite_score

    if expected["decision"] == "remove" and decision == "allow":
        raw_score -= 0.7

    if expected["decision"] == "escalate" and decision == "allow":
        raw_score -= 0.5

    final_score = max(0.0, min(raw_score, 1.0))

    breakdown = {
        "decision_score": round(decision_score, 3),
        "reasoning_score": round(reasoning_score, 3),
        "policy_score": round(policy_score, 3),
        "rewrite_score": round(rewrite_score, 3),
        "final_score": round(final_score, 3),
    }

    if final_score >= 0.85:
        feedback = "Strong moderation decision with good reasoning."
    elif final_score >= 0.5:
        feedback = "Partially correct. Reasoning or policy alignment can improve."
    else:
        feedback = "Unsafe or weak moderation judgment."

    return final_score, feedback, breakdown