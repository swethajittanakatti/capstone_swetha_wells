import json
from pathlib import Path
from datetime import datetime


def archive_document(
    document_name: str,
    classification: str,
    reason: str
):
    """
    Archive irrelevant documents.
    """

    Path("archive").mkdir(
        exist_ok=True
    )

    file_name = (
        f"archive/{document_name}.json"
    )

    data = {
        "document_name": document_name,
        "classification": classification,
        "reason": reason,
        "archived_at": datetime.now().isoformat()
    }

    with open(
        file_name,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )

    return {
        "status": "ARCHIVED",
        "file": file_name
    }