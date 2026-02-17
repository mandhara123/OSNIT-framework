import os
from newsapi import NewsApiClient
from dotenv import load_dotenv

load_dotenv()

api = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

def fetch_news():

    articles = api.get_everything(
        q="forex OR hack OR breach OR exploit OR malware",
        language="en",
        sort_by="publishedAt",
        page_size=20
    )

    results = []

    for article in articles["articles"]:
        title = article["title"]
        if title:
            results.append(title)

    return results
