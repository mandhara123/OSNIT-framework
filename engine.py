# ================= IMPORTS ================= #

from collectors.collector import collect_all
from classifier import classify_financial_attack
from enricher import enrich
from confidence import calculate_confidence
from cluster import cluster_events
from prioritizer import rank_clusters
from timeline import attach_timeline
from memory import update_history
from preprocess import clean_text
from detector import detect_threat, keywords
from scorer import score

import hashlib
from datetime import datetime


# ================= SEVERITY CLASSIFIER ================= #

def severity(score):
    if score >= 3:
        return "CRITICAL"
    elif score == 2:
        return "HIGH"
    elif score == 1:
        return "MEDIUM"
    return "LOW"


# ================= TRUSTED SOURCE WEIGHTS ================= #

TRUSTED_SOURCES = [
    "CISA",
    "NVD",
    "Exploit",
    "Krebs",
    "DarkReading",
    "BleepingComputer"
]


def get_source_weight(source):
    if not source:
        return 0

    for trusted in TRUSTED_SOURCES:
        if trusted.lower() in source.lower():
            return 2

    return 1


# ================= SAFE DATETIME PARSER ================= #

def normalize_date(date_str):

    if not date_str:
        return datetime.utcnow()

    formats = [
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue

    return datetime.utcnow()


# ================= ENGINE CORE ================= #

def run(min_score=1):

    # -------- FETCH DATA -------- #
    try:
        data = collect_all()
    except Exception as e:
        print("Collector Error:", e)
        return []

    results = []
    seen = set()

    # -------- PROCESS ARTICLES -------- #
    for article in data:

        try:
            # ---------- UNIQUE ID ---------- #
            raw_id = article.get("url") or article.get("title")

            if not raw_id:
                continue

            article_id = hashlib.md5(raw_id.encode()).hexdigest()

            if article_id in seen:
                continue
            seen.add(article_id)

            # ---------- TEXT ---------- #
            title = article.get("title", "")
            summary = article.get("summary", "")
            full_text = f"{title} {summary}"

            # ---------- CLEAN ---------- #
            cleaned = clean_text(full_text)

            # ---------- DETECTION ---------- #
            categories = detect_threat(cleaned)
            s = score(cleaned, keywords)

        except Exception as e:
            print("Processing error:", e)
            continue

        # ---------- FILTER ---------- #
        if not categories or s < min_score:
            continue

        # ---------- CLASSIFY ---------- #
        try:
            attack_type = classify_financial_attack(cleaned)
        except:
            attack_type = None

        # ---------- ENRICH ---------- #
        try:
            intel = enrich(cleaned)
        except:
            intel = {"cves": [], "ips": [], "urls": [], "malware": [], "actors": []}

        # ---------- CONFIDENCE ---------- #
        base_conf = calculate_confidence(
            score=s,
            intel=intel,
            categories=categories,
            financial_type=attack_type
        )

        source_bonus = get_source_weight(article.get("source"))
        conf = base_conf + source_bonus

        # ---------- RESULT OBJECT ---------- #
        results.append({
            "title": title,
            "summary": summary,
            "url": article.get("url"),
            "source": article.get("source"),
            "published": normalize_date(article.get("published")),

            "category": categories,
            "score": s,
            "severity": severity(s),
            "confidence": conf,
            "financial_type": attack_type,
            "intel": intel
        })

    # -------- CLUSTER -------- #
    clusters = cluster_events(results)

    # -------- PRIORITIZE -------- #
    ranked = rank_clusters(clusters)

    # -------- TIMELINE -------- #
    ranked = attach_timeline(ranked)

    # -------- MEMORY -------- #
    ranked = update_history(ranked)

    return ranked
