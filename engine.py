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


# ---------------- SEVERITY CLASSIFIER ---------------- #

def severity(score):
    if score >= 3:
        return "CRITICAL"
    elif score == 2:
        return "HIGH"
    elif score == 1:
        return "MEDIUM"
    else:
        return "LOW"


# ---------------- ENGINE CORE ---------------- #

def run(min_score=1):

    try:
        data = collect_all()
    except Exception as e:
        print("Collector Error:", e)
        return []

    results = []
    seen = set()   # prevents duplicates

    for article in data:

        # --- skip duplicates ---
        if article in seen:
            continue
        seen.add(article)

        try:
            cleaned = clean_text(article)
            categories = detect_threat(cleaned)
            s = score(cleaned, keywords)

        except Exception as e:
            print("Processing error:", e)
            continue

        # --- filtering threshold ---
        if categories and s >= min_score:
            attack_type = classify_financial_attack(cleaned)
            intel = enrich(cleaned)
            conf = calculate_confidence(s, intel, categories, attack_type)
            results.append({
                "text": article,
                "category": categories,
                "score": s,
                "severity": severity(s),
                "confidence": conf,
                "financial_type": attack_type,
                "intel": intel
            })

    # --- sort highest threat first ---
    results.sort(key=lambda x: x["confidence"], reverse=True)

    clusters = cluster_events(results)
    ranked = rank_clusters(clusters)
    ranked = attach_timeline(ranked)
    ranked = update_history(ranked)
    return ranked
