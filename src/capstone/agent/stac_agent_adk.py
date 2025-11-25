# src/capstone/agent/stac_agent_adk.py

import asyncio
import uuid

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from capstone.tools import search_satellite_scenes
from capstone.aoi.aoi_catalog import resolve_aoi
from capstone.agent.prompts import SYSTEM_PROMPT, ARGUMENT_PLANNING_INSTRUCTIONS


APP_NAME = "satellite_stac_agent"
MODEL_NAME = "gemini-2.0-flash"  # or another Gemini 2.x model available in your env

DEFAULT_SESSION_ID = f"session_{uuid.uuid4()}"
DEFAULT_USER_ID = "local_user"

def create_agent() -> Agent:
    """
    Create the root ADK Agent configured for STAC metadata search.
    """
    instruction = SYSTEM_PROMPT.strip() + "\n\n" + ARGUMENT_PLANNING_INSTRUCTIONS.strip()

    root_agent = Agent(
        name="satellite_stac_agent",
        model=MODEL_NAME,
        description="Agent to search satellite scenes via STAC based on natural language queries.",
        instruction=instruction,
        # ADK will automatically wrap these Python functions as tools.
        tools=[resolve_aoi, search_satellite_scenes],
    )
    return root_agent


async def create_runner_async(
    user_id: str = DEFAULT_USER_ID,
    session_id: str = None,
):
    if session_id is None:
        session_id = f"session_{uuid.uuid4()}"

    agent = create_agent()
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)
    return runner, session_service


def create_runner() -> tuple[Runner, InMemorySessionService]:
    """
    Sync helper: create Runner by running the async version.

    素の Python スクリプトや CLI から使う用。
    Notebook からは create_runner_async() を使う方が安全。
    """
    return asyncio.run(create_runner_async())


def call_agent(query: str) -> None:
    """
    Simple synchronous helper: send a single user query and print the final response.
    """
    runner, _ = create_runner()

    content = types.Content(role="user", parts=[types.Part(text=query)])
    events = runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content,
    )

    for event in events:
        if event.is_final_response():
            if event.content and event.content.parts:
                print("Agent Response:")
                print(event.content.parts[0].text)
