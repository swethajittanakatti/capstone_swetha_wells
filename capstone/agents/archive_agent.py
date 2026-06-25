from google.adk.agents import Agent


archive_agent = Agent(
    name="archive_agent",
    model="gemini-2.5-flash",

    description="Archives irrelevant documents",

    instruction="""
Return ONLY JSON.

{
  "action":"ARCHIVE",
  "status":"SUCCESS"
}
"""
)