from datetime import datetime

def attach_time_metadata(cluster):

    now = datetime.utcnow()

    cluster["first_seen"] = now.strftime("%Y-%m-%d %H:%M:%S")
    cluster["last_seen"] = now.strftime("%Y-%m-%d %H:%M:%S")

    cluster["event_count"] = len(cluster["events"])

    # growth logic
    if cluster["event_count"] >= 5:
        cluster["trend"] = "RAPIDLY GROWING"
    elif cluster["event_count"] >= 3:
        cluster["trend"] = "ACTIVE"
    else:
        cluster["trend"] = "LOW ACTIVITY"

    return cluster


def attach_timeline(clusters):
    return [attach_time_metadata(c) for c in clusters]
