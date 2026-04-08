import os
import requests


API_BASE_URL = os.environ["API_BASE_URL"]

def run_inference():
    try:
        
        reset_res = requests.post(f"{API_BASE_URL}/reset")
        print("Reset:", reset_res.text)

       
        step_res = requests.post(
            f"{API_BASE_URL}/step",
            json={"input": "Hello"}
        )
        print("Step:", step_res.text)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    run_inference()
