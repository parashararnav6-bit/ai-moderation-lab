import json
from pathlib import Path

def get_task():
    json_path = Path(__file__).parent / "medium.json"
    with open(json_path) as f:
        return json.load(f)
