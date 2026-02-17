from .news import fetch_news
from .rss import fetch_rss


def collect_all():

    data = []

    data += fetch_news()
    data += fetch_rss()

    return list(set(data))  # remove duplicates
