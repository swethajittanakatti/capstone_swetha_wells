from google.adk.agents import Agent


hitl_agent = Agent(
    name="hitl_agent",
    model="gemini-2.5-flash",

    description="Human review queue",

    instruction="""
Return ONLY JSON.

{
  "action":"HITL",
  "status":"PENDING_REVIEW"
}
"""
)