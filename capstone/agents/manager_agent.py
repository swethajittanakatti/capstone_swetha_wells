from google.adk.agents import Agent

from agents.classification_agent import classification_agent
from agents.database_agent import database_agent
from agents.archive_agent import archive_agent
from agents.hitl_agent import hitl_agent
from agents.audit_agent import audit_agent


manager_agent = Agent(
    name="manager_agent",
    model="gemini-2.5-flash",

    description="""
Orchestrates document processing workflow.
Routes documents based on classification.
""",

    sub_agents=[
        classification_agent,
        database_agent,
        archive_agent,
        hitl_agent,
        audit_agent,
    ],

    instruction="""
You are a workflow manager.

WORKFLOW:

1. Invoke classification_agent exactly once.

2. Read the JSON returned by classification_agent.

3. Route based on classification:

   If classification == "CEASE"
      transfer to database_agent

   If classification == "IRRELEVANT"
      transfer to archive_agent

   If classification == "UNCERTAIN"
      transfer to hitl_agent

4. Wait for the selected routing agent to finish.

5. Invoke audit_agent exactly once.

6. Return final JSON:

{
  "workflow_status": "COMPLETED",
  "classification": "<classification>",
  "action_taken": "<DATABASE_STORE|ARCHIVE|HITL>",
  "audit_status": "COMPLETED"
}

STRICT RULES:

- Never stop after classification_agent.
- Never return classification_agent output directly.
- Always invoke one routing agent.
- Always invoke audit_agent.
- Never invoke classification_agent twice.
- Never invoke more than one routing agent.
- Workflow is not complete until audit_agent runs.
- Return only final JSON.
"""
)