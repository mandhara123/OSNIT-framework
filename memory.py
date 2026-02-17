import json
import os

DB_FILE = "history.json"


# ---------------- LOAD ----------------
def load_history():
    if not os.path.exists(DB_FILE):
        return {}

    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


# ---------------- SAVE ----------------
def save_history(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


# ---------------- SAFE CLUSTER KEY ----------------
def get_cluster_key(cluster):

    # priority 1 → indicators
    if cluster.get("indicators"):
        return ",".join(sorted(cluster["indicators"]))

    # priority 2 → title
    if cluster.get("events"):
        first = cluster["events"][0]
        return first.get("title", "unknown")[:60]

    return "unknown_cluster"


# ---------------- MAIN MEMORY ENGINE ----------------
def update_history(clusters):

    history = load_history()

    for cluster in clusters:

        key = get_cluster_key(cluster)

        if key not in history:
            history[key] = {"count": 0}

        history[key]["count"] += 1
        count = history[key]["count"]

        # -------- TREND LOGIC --------
        if count >= 5:
            cluster["trend"] = "ESCALATING"
        elif count >= 3:
            cluster["trend"] = "ACTIVE"
        else:
            cluster["trend"] = "NEW"

        # attach count for dashboard
        cluster["seen_count"] = count

    save_history(history)
    return clusters
