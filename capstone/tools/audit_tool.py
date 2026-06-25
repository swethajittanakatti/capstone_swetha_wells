import json
from pathlib import Path
from datetime import datetime


def create_audit_log(
    document_name: str,
    classification: str,
    confidence: float,
    action_taken: str
):
    """
    Create audit log entry.
    """

    Path("audit_logs").mkdir(
        exist_ok=True
    )

    audit_file = (
        f"audit_logs/{datetime.now().date()}.jsonl"
    )

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "document_name": document_name,
        "classification": classification,
        "confidence": confidence,
        "action_taken": action_taken
    }

    with open(
        audit_file,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(log_entry)
            + "\n"
        )

    return {
        "status": "AUDIT_LOGGED"
    }