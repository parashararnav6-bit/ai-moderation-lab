import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://0.0.0.0:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

def run_inference():
    print("Running inference test...")

    reset_res = requests.post(f"{API_BASE_URL}/reset")
    print("Reset response:", reset_res.status_code)

    if reset_res.status_code != 200:
        print("Reset failed")
        return

    action = {
        "decision": "flag",
        "reasoning": "This content may violate policy and should be reviewed.",
        "rewrite": None
    }

    step_res = requests.post(f"{API_BASE_URL}/step", json=action)
    print("Step response:", step_res.status_code)

    if step_res.status_code == 200:
        print("Inference working ✅")
    else:
        print("Step failed ❌")

if __name__ == "__main__":
    run_inference()