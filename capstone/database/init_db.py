import sqlite3
from pathlib import Path


def initialize_database():

    Path("database").mkdir(
        exist_ok=True
    )

    conn = sqlite3.connect(
        "database/cease_requests.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cease_requests(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_name TEXT,
        received_date TEXT,
        classification TEXT,
        confidence REAL,
        reason TEXT,
        action_taken TEXT,
        processed_timestamp TEXT           
    )
    """)

    conn.commit()
    conn.close()

    print("Database initialized")


if __name__ == "__main__":
    initialize_database()