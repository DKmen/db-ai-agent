from langgraph.prebuilt import create_react_agent
from app.helper import llm
from .tools import fetch_schema, run_query
from app.constants import db_agent_prompt

db_assistant = create_react_agent(
    name="db_assistant",
    model=llm,
    tools=[fetch_schema, run_query],
    prompt=db_agent_prompt,
)
