import re


# ---------------- CVE EXTRACTOR ---------------- #

def extract_cves(text):
    pattern = r"CVE-\d{4}-\d{4,7}"
    return re.findall(pattern, text)


# ---------------- IP ADDRESS EXTRACTOR ---------------- #

def extract_ips(text):
    pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    return re.findall(pattern, text)


# ---------------- URL EXTRACTOR ---------------- #

def extract_urls(text):
    pattern = r"https?://[^\s]+"
    return re.findall(pattern, text)


# ---------------- MALWARE NAME DETECTOR ---------------- #

known_malware = [
    "emotet", "trickbot", "dridex", "agenttesla", "redline",
    "lumma", "warlock", "glassworm", "ninjabrowser",
    "voidlink", "canfail"
]

def detect_malware(text):
    found = []
    for name in known_malware:
        if name in text.lower():
            found.append(name)
    return found


# ---------------- THREAT ACTOR DETECTOR ---------------- #

known_actors = [
    "apt28", "apt29", "lazarus", "sandworm", "cozybear",
    "fancybear", "tgr-sta", "china-linked", "state-backed"
]

def detect_actors(text):
    found = []
    for actor in known_actors:
        if actor in text.lower():
            found.append(actor)
    return found


# ---------------- MASTER ENRICH FUNCTION ---------------- #

def enrich(text):

    return {
        "cves": extract_cves(text),
        "ips": extract_ips(text),
        "urls": extract_urls(text),
        "malware": detect_malware(text),
        "actors": detect_actors(text)
    }
