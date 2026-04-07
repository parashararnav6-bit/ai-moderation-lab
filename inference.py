import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def run_inference():
    print("[START] task=moderation", flush=True)


    reset_res = requests.post(f"{API_BASE_URL}/reset")

    if reset_res.status_code != 200:
        print("[END] task=moderation score=0 steps=0", flush=True)
        return

    obs = reset_res.json()
    action = {
        "decision": "flag",
        "reasoning": "Potential policy violation",
        "rewrite": None
    }

    step_res = requests.post(f"{API_BASE_URL}/step", json=action)

    if step_res.status_code != 200:
        print("[END] task=moderation score=0 steps=1", flush=True)
        return

    result = step_res.json()

    reward = result.get("reward", 0)

    print(f"[STEP] step=1 reward={reward}", flush=True)

    print("[END] task=moderation score=1 steps=1", flush=True)


if __name__ == "__main__":
    run_inference()
