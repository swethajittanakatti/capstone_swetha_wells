# Corrected main.py
# Routes:
# CEASE -> database_agent
# IRRELEVANT -> archive_agent
# UNCERTAIN -> hitl_agent
# Always -> audit_agent

import uuid
import asyncio
import json
from pathlib import Path
from datetime import datetime

from google.genai import types
from google.genai.errors import ServerError
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from root_agent import root_agent
from tools.document_loader_tool import load_document
from database.init_db import initialize_database

from agents.database_agent import database_agent
from agents.archive_agent import archive_agent
from agents.hitl_agent import hitl_agent
from agents.audit_agent import audit_agent

APP_NAME = "cease_processing"
USER_ID = "swetha"

PDF_FOLDER = Path("data/pdfs")
OUTPUT_FOLDER = Path("output")

MAX_RETRIES = 5
OUTPUT_FOLDER.mkdir(exist_ok=True)


async def execute_agent(agent, session_service, document_text, pdf_name):

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=str(uuid.uuid4())
    )

    runner = Runner(
        app_name=APP_NAME,
        agent=agent,
        session_service=session_service
    )

    content = types.Content(
        role="user",
        parts=[
            types.Part(
                text=f"""
Document Name:
{pdf_name}

Document Content:
{document_text}
"""
            )
        ]
    )

    response_text = ""

    events = runner.run(
        user_id=USER_ID,
        session_id=session.id,
        new_message=content
    )

    for event in events or []:

        if event.content:

            for part in getattr(event.content, "parts", []) or []:

                text = getattr(part, "text", None)

                if text:
                    response_text += text

    return response_text


async def process_document(runner, session_service, pdf_path):

    print("\\n" + "=" * 80)
    print(f"Processing: {pdf_path.name}")
    print("=" * 80)

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=str(uuid.uuid4())
    )

    try:

        document_text = load_document(str(pdf_path))

        if not document_text.strip():
            print("No text extracted.")
            return

        content = types.Content(
            role="user",
            parts=[
                types.Part(
                    text=f"""
Document Name:
{pdf_path.name}

Document Content:
{document_text}
"""
                )
            ]
        )

        success = False

        for attempt in range(MAX_RETRIES):

            try:

                events = runner.run(
                    user_id=USER_ID,
                    session_id=session.id,
                    new_message=content
                )

                agent_outputs = []
                classification_json = None

                for event in events:

                    print(f"\\nAgent: {event.author}")

                    event_record = {
                        "agent": event.author,
                        "content": ""
                    }

                    if event.content:

                        for part in getattr(event.content, "parts", []):

                            text = getattr(part, "text", None)

                            if text:

                                print(text)
                                print("DEBUG AUTHOR =", event.author)
                                event_record["content"] += text

                                if event.author == "classification_agent":

                                    try:

                                        cleaned = (
                                            text.replace("```json", "")
                                            .replace("```", "")
                                            .strip()
                                        )

                                        classification_json = json.loads(cleaned)
                                        print("DEBUG classification_json =", classification_json)
                                    except Exception:
                                        pass

                    agent_outputs.append(event_record)

                classification = "UNCERTAIN"

                if classification_json:
                    classification = classification_json.get(
                        "classification",
                        "UNCERTAIN"
                    )
                print(f"ROUTING DECISION = {classification}")
                routing_response = ""
                action_taken = ""

                if classification == "CEASE":
                    print("******** CALLING DATABASE AGENT ********")
                    routing_response = await execute_agent(
                        database_agent,
                        session_service,
                        json.dumps(classification_json, indent=2),
                        pdf_path.name
                    )
                    print("\nDATABASE RESPONSE:")
                    print(routing_response)
                    action_taken = "DATABASE"
                    
                elif classification == "IRRELEVANT":
                    print("\n******** CALLING ARCHIVE AGENT ********")
                    routing_response = await execute_agent(
                        archive_agent,
                        session_service,
                        json.dumps(classification_json, indent=2),
                        pdf_path.name
                    )
                    print("\nARCHIVE RESPONSE:")
                    print(routing_response)
                    action_taken = "ARCHIVE"

                else:
                    print("\n******** CALLING HITL AGENT ********")
                    routing_response = await execute_agent(
                        hitl_agent,
                        session_service,
                        json.dumps(classification_json, indent=2),
                        pdf_path.name
                    )
                    print("\nHITL RESPONSE:")
                    print(routing_response)
                    action_taken = "HITL"
                print("\n******** CALLING AUDIT AGENT ********")
                audit_response = await execute_agent(
                    audit_agent,
                    session_service,
                    f"""
Classification:
{json.dumps(classification_json, indent=2)}

Action Taken:
{action_taken}

Routing Response:
{routing_response}
""",
                    pdf_path.name
                )
                print("\nAUDIT RESPONSE:")
                print(audit_response)
                output_data = {
                    "file_name": pdf_path.name,
                    "processed_at": datetime.now().isoformat(),
                    "classification": classification_json,
                    "action_taken": action_taken,
                    "routing_response": routing_response,
                    "audit_response": audit_response,
                    "agent_outputs": agent_outputs
                }

                output_file = OUTPUT_FOLDER / f"{pdf_path.stem}.json"

                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(
                        output_data,
                        f,
                        indent=2,
                        ensure_ascii=False
                    )

                print(f"Saved: {output_file}")

                success = True
                break

            except ServerError as e:

                if "503" in str(e):

                    wait_time = (attempt + 1) * 15
                    await asyncio.sleep(wait_time)

                else:
                    raise

        if not success:
            print("Failed after retries.")

    except Exception as e:

        print(f"ERROR: {e}")


async def main():

    initialize_database()

    session_service = InMemorySessionService()

    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service
    )

    pdf_files = list(PDF_FOLDER.glob("*.pdf"))

    for pdf in pdf_files:

        await process_document(
            runner,
            session_service,
            pdf
        )

        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
