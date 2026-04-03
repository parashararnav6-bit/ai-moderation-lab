import json


def load_task(level):
    with open(f"data/{level}.json", "r", encoding="utf-8") as f:
        return json.load(f)