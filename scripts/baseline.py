import os
from openai import OpenAI

from env.environment import ModerationEnv
from env.models import Action

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_decision(text: str) -> str:
    lower = text.lower()
    for option in ["remove", "escalate", "flag", "allow"]:
        if option in lower:
            return option
    return "flag"


def run_level(level: str):
    env = ModerationEnv(level=level)
    obs = env.reset()
    done = False
    total = 0.0
    steps = 0

    while not done:
        prompt = f"""
You are an AI trust and safety moderator.

Post: {obs.post}
Context: {obs.context}
User history: {obs.user_history}

Choose one decision: allow, flag, remove, or escalate.
Then explain the policy reasoning in 2-4 sentences.
Optionally include a safer rewrite.
"""
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        output = res.choices[0].message.content
        decision = extract_decision(output)

        action = Action(
            decision=decision,
            reasoning=output,
            rewrite=None,
        )

        obs, reward, done, _ = env.step(action)
        total += reward.score
        steps += 1

    avg = total / steps if steps else 0.0
    return round(avg, 3)


if __name__ == "__main__":
    for level in ["easy", "medium", "hard"]:
        score = run_level(level)
        print(f"{level}: {score}")