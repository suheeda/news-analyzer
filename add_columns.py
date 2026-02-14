import sqlite3

# Path to your SQLite database
DB_PATH = "news.db"

# List of required columns and their types
required_columns = {
    "sentiment": "TEXT",
    "sentiment_compound": "REAL"  # Add other columns if needed
}

def add_missing_columns(db_path, columns_dict):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get existing columns
    cursor.execute("PRAGMA table_info(articles);")
    existing_columns = [col[1] for col in cursor.fetchall()]
    print("Existing columns:", existing_columns)

    # Add missing columns
    for column_name, column_type in columns_dict.items():
        if column_name not in existing_columns:
            alter_sql = f"ALTER TABLE articles ADD COLUMN {column_name} {column_type}"
            cursor.execute(alter_sql)
            print(f"Added column: {column_name} ({column_type})")
        else:
            print(f"Column already exists: {column_name}")

    conn.commit()
    conn.close()
    print("All missing columns processed successfully.")

if __name__ == "__main__":
    add_missing_columns(DB_PATH, required_columns)
