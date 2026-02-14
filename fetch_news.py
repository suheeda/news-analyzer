import os
import requests
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from etl_store import engine, Article, init_db

API_KEY = os.getenv("NEWS_API_KEY", "7a96a14ea46d46e481849d3024d03d7f")  # Replace with your key or set in .env
NEWS_API_URL = "https://newsapi.org/v2/everything"

SessionLocal = sessionmaker(bind=engine, future=True)

def fetch_news(query="technology", page_size=10):
    """Fetch news from NewsAPI and save into DB."""
    init_db()
    session = SessionLocal()

    url = f"{NEWS_API_URL}?q={query}&pageSize={page_size}&apiKey={API_KEY}"
    resp = requests.get(url)
    data = resp.json()

    added = 0
    if data.get("status") == "ok":
        for a in data["articles"]:
            if session.query(Article).filter_by(url=a.get("url")).first():
                continue
            published = None
            if a.get("publishedAt"):
                try:
                    published = datetime.fromisoformat(a["publishedAt"].replace("Z", "+00:00"))
                except:
                    pass
            art = Article(
                source=(a.get("source") or {}).get("name"),
                author=a.get("author"),
                title=a.get("title"),
                description=a.get("description"),
                url=a.get("url"),
                published_at=published,
                content=a.get("content"),
                topic=query
            )
            session.add(art)
            added += 1
        session.commit()

    session.close()
    print(f"✅ Stored {added} new '{query}' articles")

def fetch_and_store(query="technology", page_size=10):
    """Wrapper so Streamlit can call this easily."""
    fetch_news(query=query, page_size=page_size)
