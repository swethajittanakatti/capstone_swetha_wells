from google.adk.agents import Agent

extraction_agent = Agent(
    name="extraction_agent",
    model="gemini-2.5-flash",

    description="Extract structured cease notice details",

    instruction="""
Extract key information from the document.

Return ONLY JSON.

{
  "sender":"",
  "recipient":"",
  "claim_type":"",
  "deadline":"",
  "demands":[],
  "legal_threat":false
}
"""
)