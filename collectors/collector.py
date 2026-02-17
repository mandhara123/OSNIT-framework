from .rss import fetch_rss
# from .news import fetch_news  (if you have one)

def collect_all():

    data = []

    try:
        data.extend(fetch_rss())
    except Exception as e:
        print("RSS error:", e)

    # if you have other collectors add them here
    # try:
    #     data.extend(fetch_news())
    # except Exception as e:
    #     print("News error:", e)

    # -------- REMOVE DUPLICATES SAFELY -------- #
    unique = {}
    for article in data:

        key = article.get("url") or article.get("title")

        if key:
            unique[key] = article

    return list(unique.values())
