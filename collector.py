import os
import logging
import feedparser
from newsapi import NewsApiClient
from dotenv import load_dotenv
from .keywords import KEYWORDS
from .sources import RSS_FEEDS

load_dotenv()

logging.basicConfig(level=logging.INFO)

# ---------- API CLIENTS ----------

news_api = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))


# ---------- HELPERS ----------

def contains_keyword(text):
    text = text.lower()
    return any(word in text for word in KEYWORDS)

def deduplicate(items):
    return list(set(items))


# ---------- NEWS SOURCE ----------

def fetch_news():
    try:
        query = " OR ".join(KEYWORDS)

        articles = news_api.get_everything(
            q=query,
            language="en",
            sort_by="publishedAt",
            page_size=30
        )

        results = [
            a["title"]
            for a in articles["articles"]
            if contains_keyword(a["title"])
        ]

        logging.info(f"News collected: {len(results)}")
        return results

    except Exception as e:
        logging.error(f"News API Error: {e}")
        return []





# ---------- RSS SOURCE ----------

def fetch_rss():
    results = []

    try:
        for url in RSS_FEEDS:
            feed = feedparser.parse(url)

            for entry in feed.entries:
                if contains_keyword(entry.title):
                    results.append(entry.title)

        logging.info(f"RSS collected: {len(results)}")
        return results

    except Exception as e:
        logging.error(f"RSS Error: {e}")
        return []


# ---------- MASTER COLLECTOR ----------

def collect_all():
    logging.info("Starting OSINT collection...")

    data = []
    data.extend(fetch_news())
    data.extend(fetch_rss())

    data = deduplicate(data)

    logging.info(f"Total collected: {len(data)}")

    return data
