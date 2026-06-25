from google.adk.agents import Agent


audit_agent = Agent(
    name="audit_agent",
    model="gemini-2.5-flash",

    description="Creates workflow audit log",

    instruction="""
Create audit result.

Return ONLY JSON.

{
  "audit_status":"COMPLETED"
}
"""
)