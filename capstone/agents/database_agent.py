from google.adk.agents import Agent
from tools.database_tool import save_cease_request

database_agent = Agent(
    name="database_agent",
    model="gemini-2.5-flash",

    tools=[save_cease_request],

    description="Store cease request",

    instruction="""
Store the cease request.

Call save_cease_request exactly once.

Return ONLY JSON.

{
  "action":"DATABASE_STORE",
  "status":"SUCCESS"
}
"""
)