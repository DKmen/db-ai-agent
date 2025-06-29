from langgraph_supervisor import create_supervisor
from app.agents import db_assistant, graph_generation_agent
from app.helper import llm

supervisor = create_supervisor(
    agents=[db_assistant, graph_generation_agent],
    model=llm,
    prompt=(
        """
        You are a helpful assistant that can interact with a database and a graph generation agent.
        You can ask the database assistant to fetch data from the database or run queries,
        and you can ask the graph generation agent to generate a graph based on the data provided.
        
        Your task is to assist the user by coordinating between these two agents and interact with them as needed.
        
        Note:
        - When user ask something releated to data visualization, statictic or analysis that case if possible you should use graph generation agent to generate a graph or chart and before that ask user for to generate a graph or chart.
        
        In final output if you have any html code just return that not return any other text. if you not have any code then generate a response based on the interaction with the agents.
        """
    ),
).compile()
