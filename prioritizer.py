def calculate_priority(cluster):
    score = 0

    for event in cluster["events"]:

        # Severity weight
        sev = event["severity"]
        if sev == "CRITICAL":
            score += 5
        elif sev == "HIGH":
            score += 3
        elif sev == "MEDIUM":
            score += 2
        else:
            score += 1

        # Confidence weight
        score += event["confidence"]

        # Financial threat bonus
        if event["financial_type"]:
            score += 3

    return score


def rank_clusters(clusters):

    for cluster in clusters:
        cluster["priority_score"] = calculate_priority(cluster)

    return sorted(clusters, key=lambda x: x["priority_score"], reverse=True)
