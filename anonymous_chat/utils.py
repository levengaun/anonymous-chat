import json


def load_json(filepath):
    with open(filepath, "r", encoding="utf8") as f:
        return json.load(f)


def save_json(data, filepath):
    with open(filepath, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)


def load_txt(filepath):
    with open(filepath, "r", encoding="utf8") as f:
        return f.read().splitlines()