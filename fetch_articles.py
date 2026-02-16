import os
from newsapi import NewsApiClient
from etl_store import save_articles

# Try both environment and fallback
API_KEY = os.getenv("NEWSAPI_KEY")

# If Railway variable fails, you can paste key here temporarily
FALLBACK_KEY = "7a96a14ea46d46e481849d3024d03d7f"

if not API_KEY:
    API_KEY = FALLBACK_KEY

if not API_KEY:
    print("⚠ NEWSAPI_KEY missing. Skipping fetch.")
    def main():
        return
else:
    newsapi = NewsApiClient(api_key=API_KEY)

    TOPICS = ["general", "technology", "business", "sports", "entertainment"]

    def fetch_live_articles():
        all_articles = []

        for topic in TOPICS:
            try:
                response = newsapi.get_top_headlines(
                    category=topic,
                    language="en",
                    page_size=20
                )
            except Exception as e:
                print("NewsAPI error:", e)
                continue

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