import os
from newsapi import NewsApiClient
from etl_store import save_articles
from datetime import datetime

# ✅ 1. Set your API key here (used if environment variable not set)
DEFAULT_API_KEY = "7a96a14ea46d46e481849d3024d03d7f"  # <-- replace with your actual key

# 2. Read API key from environment variable if available
API_KEY = os.getenv("NEWSAPI_KEY") or DEFAULT_API_KEY

if not API_KEY:
    raise ValueError("No NewsAPI key provided. Set NEWSAPI_KEY env variable or DEFAULT_API_KEY in code.")

# 3. Initialize NewsAPI
newsapi = NewsApiClient(api_key=API_KEY)

# 4. Define topics
TOPICS = ["general", "technology", "business", "sports", "entertainment"]

def fetch_live_articles():
    all_articles = []

    for topic in TOPICS:
        response = newsapi.get_top_headlines(
            category=topic,
            language="en",
            page_size=20
        )

        for article in response.get("articles", []):
            if not article.get("url"):
                continue  # skip if URL is missing

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

# 5. Fetch and save articles
if __name__ == "__main__":
    articles = fetch_live_articles()
    save_articles(articles)
    print(f"Saved {len(articles)} live articles to the database.")
