def get_indicators(item):
    intel = item["intel"]

    return set(
        intel["cves"] +
        intel["ips"] +
        intel["urls"] +
        intel["malware"] +
        intel["actors"]
    )


def cluster_events(results):

    clusters = []

    for item in results:

        indicators = get_indicators(item)

        matched = False

        for cluster in clusters:

            # match if share indicator
            if indicators & cluster["indicators"]:

                cluster["events"].append(item)
                cluster["count"] += 1
                cluster["indicators"].update(indicators)

                matched = True
                break

        if not matched:
            clusters.append({
                "indicators": set(indicators),
                "events": [item],
                "count": 1
            })

    return clusters
