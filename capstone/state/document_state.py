from pydantic import BaseModel


class DocumentState(BaseModel):

    document_name: str

    classification: str | None = None

    confidence: float | None = None

    reason: str | None = None

    action_taken: str | None = None

    audit_status: str | None = None