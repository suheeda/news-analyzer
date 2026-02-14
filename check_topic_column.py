import sqlite3

DB_PATH = "news.db"
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
