import sqlite3
from datetime import datetime

DB_PATH = "database/cease_requests.db"


def save_cease_request(
    document_name: str,
    classification: str,
    confidence: float,
    reason: str
):
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO cease_requests
        (
            document_name,
            received_date,
            classification,
            confidence,
            reason
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            document_name,
            datetime.now().isoformat(),
            classification,
            confidence,
            reason
        )
    )

    conn.commit()

    row_id = cursor.lastrowid

    conn.close()

    return {
        "status": "saved",
        "record_id": row_id
    }