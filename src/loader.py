import json

def load_candidates(path):
    candidates = []

    with open(path, "r") as f:
        for line in f:
            if line.strip():
                candidates.append(json.loads(line))

    return candidates