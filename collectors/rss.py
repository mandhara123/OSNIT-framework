import feedparser

RSS_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://www.darkreading.com/rss.xml"
]

def fetch_rss():

    results = []

    for url in RSS_FEEDS:

        feed = feedparser.parse(url)

        for entry in feed.entries:
            results.append(entry.title)

    return results
