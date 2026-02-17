keywords = {
    "Account Hijacking": ["hijacking","takeover","breach","unauthorized"],
    "Forex Scam": ["forexscam","ponzi","withdrawal","deposit"],
    "Malware Attack": ["exploit","cve","payload","backdoor","malware"]
}

def detect_threat(text):
    matches = []

    for category, words in keywords.items():
        for word in words:
            if word in text:
                matches.append(category)

    return list(set(matches))
