def calculate_confidence(score, intel, categories, financial_type):

    confidence = 0

    # keyword strength
    confidence += score

    # CVE presence = strong technical proof
    if intel["cves"]:
        confidence += 3

    # threat actor attribution
    if intel["actors"]:
        confidence += 3

    # malware identification
    if intel["malware"]:
        confidence += 2

    # financial relevance
    if financial_type:
        confidence += 2

    # multiple threat categories detected
    if len(categories) > 1:
        confidence += 1

    return confidence
