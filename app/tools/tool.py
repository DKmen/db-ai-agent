from langchain.tools import Tool

from app.tools.fetchSchema import fetch_schema
from app.tools.runFetchQuery import run_query

tools = [
    Tool(
        name="fetch_db_schema",
        func= fetch_schema,
        description="Returns the PostgreSQL schema (table names and columns)."
    ),
    Tool(
        name="run_query",
        func=run_query,
        description="Run a SQL query against PostgreSQL and return the result."
    ),
]