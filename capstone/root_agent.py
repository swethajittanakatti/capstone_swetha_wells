from google.adk.agents import Agent

from agents.manager_agent import manager_agent

root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",

    sub_agents=[
        manager_agent
    ],

    description="Entry point for document processing",

    instruction="""
    You are the root agent.

    The user message already contains:

    - Document Name
    - Extracted Document Content

    Your responsibilities:

    1. Review the document information.
    2. Delegate processing to manager_agent.
    3. Return the final result.

    Always use manager_agent for document processing.
    """
)