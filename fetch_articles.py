import os
from newsapi import NewsApiClient
from etl_store import save_articles

API_KEY = os.getenv("7a96a14ea46d46e481849d3024d03d7f")

TOPICS = ["general", "technology", "business", "sports", "entertainment"]


def fetch_live_articles():
    if not API_KEY:
        print("NEWSAPI_KEY not found. Skipping fetch.")
        return []

    newsapi = NewsApiClient(api_key=API_KEY)
    all_articles = []

    for topic in TOPICS:
        response = newsapi.get_top_headlines(
            category=topic,
            language="en",
            page_size=20
        )

        for article in response.get("articles", []):
            if not article.get("url"):
                continue

            all_articles.append({
                "source": article["source"]["name"] if article.get("source") else "Unknown",
                "author": article.get("author"),
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url"),
                "publishedAt": article.get("publishedAt"),
                "content": article.get("content"),
                "topic": topic
            })

    return all_articles


def main():
    articles = fetch_live_articles()
    if articles:
        save_articles(articles)
        print(f"Saved {len(articles)} articles.")
    else:
        print("No articles fetched.")