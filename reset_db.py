import os
import time
import sqlite3
from datetime import datetime

DB_PATH = "news.db"
LOG_FILE = "db_reset.log"

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(message)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

# Step 1: Try to rename the old database
BACKUP_PATH = f"news_backup_{int(time.time())}.db"
try:
    if os.path.exists(DB_PATH):
        os.rename(DB_PATH, BACKUP_PATH)
        log(f"Old database renamed to: {BACKUP_PATH}")
    else:
        log("No existing database found.")
except PermissionError:
    log("Database is currently in use. Attempting to close connections...")
    try:
        # Attempt to open a connection in exclusive mode to break locks
        con = sqlite3.connect(DB_PATH, timeout=1)
        con.close()
        os.rename(DB_PATH, BACKUP_PATH)
        log(f"Old database renamed to: {BACKUP_PATH}")
    except Exception as e:
        log(f"Failed to reset database. Close all apps using it and try again.\n{e}")
        exit(1)

# Step 2: Create a new database with correct schema
from sqlalchemy import create_engine
from models import Base

try:
    engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
    Base.metadata.create_all(engine)
    log("New database created successfully!")
except Exception as e:
    log(f"Failed to create new database.\n{e}")
    exit(1)
