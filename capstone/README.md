# Capstone project 
'''bash
python -m venv .venv
source .venv.bin/activate
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# CEASE Document Processing System

## Overview

This project is an AI-powered document processing pipeline built using Google ADK and Gemini.

The system processes PDF documents, classifies them as legal cease-and-desist related documents or non-relevant documents, routes them to the appropriate workflow, records audit information, and generates structured JSON output.

---

# Architecture

## High-Level Workflow

```text
PDF Document
      │
      ▼
Document Loader
      │
      ▼
root_agent
      │
      ▼
manager_agent
      │
      ▼
classification_agent
      │
      ▼
main.py Routing Logic
      │
      ├──────────────► database_agent
      │
      ├──────────────► archive_agent
      │
      └──────────────► hitl_agent
                               │
                               ▼
                         audit_agent
                               │
                               ▼
                         JSON Output
```

---

# Components

## root_agent

Responsibilities:

* Entry point for all documents.
* Transfers document processing to manager_agent.
* Does not perform classification.
* Does not perform routing.

---

## manager_agent

Responsibilities:

* Workflow coordinator.
* Invokes classification_agent.
* Returns classification result.

Responsibilities NOT handled by manager_agent:

* Database storage
* Archiving
* Human review
* Audit logging

These actions are executed by main.py.

---

## classification_agent

Purpose:

Analyze document contents and classify the document.

Possible classifications:

### CEASE

Examples:

* Cease and Desist Letters
* Copyright Infringement Notices
* Trademark Violations
* Takedown Requests
* Legal Demands

### IRRELEVANT

Examples:

* Invoices
* Appointment Letters
* Informational Documents
* Audit Reports

### UNCERTAIN

Examples:

* Poor OCR quality
* Missing information
* Ambiguous legal language

Output:

```json
{
  "classification": "CEASE",
  "confidence": 0.95,
  "reason": "",
  "sender": "",
  "recipient": "",
  "document_type": "",
  "deadline": "",
  "summary": ""
}
```

---

## database_agent

Executed when:

```text
classification = CEASE
```

Responsibilities:

* Process classified legal documents.
* Store extracted metadata.
* Prepare structured records for database persistence.

---

## archive_agent

Executed when:

```text
classification = IRRELEVANT
```

Responsibilities:

* Archive non-relevant documents.
* Record archival metadata.

---

## hitl_agent

Executed when:

```text
classification = UNCERTAIN
```

Responsibilities:

* Flag document for human review.
* Generate review request.

HITL = Human In The Loop

---

## audit_agent

Executed for every processed document.

Responsibilities:

* Generate audit records.
* Track workflow execution.
* Record classification outcome.
* Maintain processing history.

---

# Routing Logic

Routing is implemented in main.py.

```python
if classification == "CEASE":
    database_agent

elif classification == "IRRELEVANT":
    archive_agent

else:
    hitl_agent

audit_agent
```

This approach guarantees deterministic workflow execution and avoids relying on LLM-based routing decisions.

---

# Project Structure

```text
project/

├── agents/
│   ├── root_agent.py
│   ├── manager_agent.py
│   ├── classification_agent.py
│   ├── database_agent.py
│   ├── archive_agent.py
│   ├── hitl_agent.py
│   └── audit_agent.py
│
├── tools/
│   ├── document_loader_tool.py
│   └── ocr_tool.py
│
├── database/
│   ├── init_db.py
│   └── cease_documents.db
│
├── data/
│   └── pdfs/
│
├── output/
│
├── main.py
│
└── README.md
```

---

# Processing Steps

1. Load PDF document.
2. Extract text using OCR if required.
3. Send document to root_agent.
4. root_agent transfers to manager_agent.
5. manager_agent invokes classification_agent.
6. classification result returned.
7. main.py evaluates classification.
8. Route to database_agent, archive_agent, or hitl_agent.
9. Execute audit_agent.
10. Save workflow output as JSON.

---

# Output Example

```json
{
  "file_name": "copyright_notice.pdf",
  "classification": "CEASE",
  "action_taken": "DATABASE_STORE",
  "audit_status": "COMPLETED",
  "processed_at": "2026-06-25T10:30:00"
}
```

---

# Current Implementation Status

| Component            | Status   |
| -------------------- | -------- |
| PDF Loading          | Complete |
| OCR Support          | Complete |
| root_agent           | Complete |
| manager_agent        | Complete |
| classification_agent | Complete |
| Python Routing       | Complete |
| database_agent       | Complete |
| archive_agent        | Complete |
| hitl_agent           | Complete |
| audit_agent          | Complete |
| JSON Output          | Complete |

---

# Future Enhancements

* Database persistence to PostgreSQL.
* Vector search for legal documents.
* Dashboard for audit review.
* Human review portal.
* Batch parallel processing.
* Document version tracking.
* Workflow monitoring and metrics.
