import json
from pathlib import Path

def get_task():
    json_path = Path(__file__).parent / "hard.json"
    with open(json_path) as f:
        dataset = json.load(f)
    
    return {
        "name": "moderation_hard",
        "description": "Hard moderation cases",
        "dataset": dataset,
        "grader": {
            "type": "custom",
            "script": "inference.py",
            "metric": "decision_accuracy"
        }
    }
