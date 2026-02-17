import feedparser

RSS_FEEDS = [
    # --- REAL ATTACK INTEL ---
    "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml",
    "https://www.cisa.gov/news.xml",
    "https://www.exploit-db.com/rss.xml",

    # --- SECURITY NEWS ---
    "https://feeds.feedburner.com/TheHackersNews",
    "https://krebsonsecurity.com/feed/",
    "https://www.bleepingcomputer.com/feed/",
    "https://www.darkreading.com/rss.xml"
]


def fetch_rss():

    results = []

    for url in RSS_FEEDS:

        feed = feedparser.parse(url)

        source_name = feed.feed.title if "title" in feed.feed else url

        for entry in feed.entries:

            results.append({
                "title": entry.title if "title" in entry else "",

                "summary":
                    entry.summary if "summary" in entry
                    else entry.description if "description" in entry
                    else "",

                "url": entry.link if "link" in entry else "",

                "source": source_name,

                "published":
                    entry.published if "published" in entry
                    else entry.updated if "updated" in entry
                    else ""
            })

    return results
