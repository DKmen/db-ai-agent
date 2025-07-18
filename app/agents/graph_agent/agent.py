from pydantic import BaseModel

from langgraph.prebuilt import create_react_agent
from app.helper import llm
from app.constants import graph_agent_prompt

class OutputSchema(BaseModel):
    """
    Output schema for the database assistant.
    Contains the schema of the database and the results of executed queries.
    """
    results: str

graph_generation_agent = create_react_agent(
    name="graph_generation_agent",
    model=llm,
    tools=[],
    prompt=graph_agent_prompt,
    response_format=OutputSchema,
)
