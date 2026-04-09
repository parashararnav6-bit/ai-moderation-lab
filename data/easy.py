import json
from pathlib import Path

def get_task():
    json_path = Path(__file__).parent / "easy.json"
    with open(json_path) as f:
        tasks = json.load(f)
    
    return {
        "name": "moderation_easy",
        "description": "Easy moderation cases",
        "dataset": tasks,
        "grader": {
            "type": "custom",
            "script": "inference.py",
            "metric": "decision_accuracy"
        }
    }