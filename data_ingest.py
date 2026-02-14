import requests
from datetime import datetime
from etl_store import save_articles

NEWS_API_KEY = "YOUR_NEWSAPI_KEY"
NEWS_API_URL = "https://newsapi.org/v2/everything"

def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        return None

def fetch_articles(query, page_size=10, page=1):
    params = {
        "q": query,
        "pageSize": page_size,
        "page": page,
        "apiKey": "7a96a14ea46d46e481849d3024d03d7f"
    }
    resp = requests.get(NEWS_API_URL, params=params).json()
    articles = []
    for item in resp.get("articles", []):
        articles.append({
            "source": item.get("source", {}).get("name"),
            "author": item.get("author"),
            "title": item.get("title"),
            "description": item.get("description"),
            "url": item.get("url"),
            "published_at": parse_date(item.get("publishedAt")),
            "content": item.get("content")
        })
    return articles

def fetch_and_store(query, page_size=10, pages=1):
    total = 0
    for page in range(1, pages+1):
        arts = fetch_articles(query, page_size=page_size, page=page)
        save_articles(arts)
        total += len(arts)
    print(f"Saved {total} articles for query '{query}'")
