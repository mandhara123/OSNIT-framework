import json
import os

DB_FILE = "history.json"


def load_history():
    if not os.path.exists(DB_FILE):
        return {}

    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_history(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


def update_history(clusters):

    history = load_history()

    for cluster in clusters:

        key = ",".join(sorted(cluster["indicators"])) or cluster["events"][0]["text"][:40]

        if key not in history:
            history[key] = {
                "count": 0
            }

        history[key]["count"] += 1

        # trend calculation
        if history[key]["count"] >= 5:
            cluster["trend"] = "ESCALATING"
        elif history[key]["count"] >= 3:
            cluster["trend"] = "ACTIVE"
        else:
            cluster["trend"] = "NEW"

    save_history(history)
    return clusters
