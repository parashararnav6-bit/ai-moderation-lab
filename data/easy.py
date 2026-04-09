import json
from pathlib import Path

def get_task():
    json_path = Path(__file__).parent / "easy.json"
    with open(json_path) as f:
        dataset = json.load(f)
    
    return {
        "name": "moderation_easy",
        "description": "Easy moderation cases",
        "dataset": dataset,
        "grader": {
            "type": "custom",
            "script": "inference.py",
            "metric": "decision_accuracy"
        }
    }
