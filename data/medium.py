import json
from pathlib import Path

def get_task():
    json_path = Path(__file__).parent / "medium.json"
    with open(json_path) as f:
        tasks = json.load(f)
    
    return {
        "name": "moderation_medium",
        "description": "Medium moderation cases",
        "dataset": tasks,
        "grader": {
            "type": "custom",
            "script": "inference.py",
            "metric": "decision_accuracy"
        }
    }