# update_db.py
import sqlite3
from etl_store import save_articles, fetch_newsapi_articles

DB_PATH = "news.db"
API_KEY = "YOUR_NEWSAPI_KEY"  # <-- Replace with your NewsAPI key

# --- Ensure topic column exists ---
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(articles)")
columns = [col[1] for col in cursor.fetchall()]

if "topic" not in columns:
    print("Adding 'topic' column to articles table...")
    cursor.execute("ALTER TABLE articles ADD COLUMN topic TEXT DEFAULT 'general'")
    conn.commit()
    print("'topic' column added successfully!")
else:
    print("'topic' column already exists.")
conn.close()

# --- Fetch real articles from NewsAPI ---
topics = ["general", "technology", "business", "sports", "health"]
total_saved = 0

for topic in topics:
    articles = fetch_newsapi_articles(API_KEY, query=topic, page_size=20)
    save_articles(articles)
    total_saved += len(articles)

print(f"Saved {total_saved} new articles to the database.")
