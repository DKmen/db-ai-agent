from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict
from sqlalchemy import text
from langchain_core.tools import tool

from sqlmodel import create_engine

@tool
def run_query(db_connection_url: str,query: str) -> List[Dict]:
    """
        Execute a SELECT query on a database and return the results as a list of dictionaries.
        This function connects to a database using the provided connection URL, executes a SELECT query,
        and returns the results in a structured format. Only SELECT statements are allowed for security
        reasons to prevent data modification operations.
        Args:
            db_connection_url (str): Database connection URL in the format supported by SQLAlchemy
                                (e.g., 'postgresql://user:password@host:port/database')
            query (str): SQL SELECT query string to execute
        Returns:
            List[Dict]: A list of dictionaries where each dictionary represents a row from the query result.
                    Each dictionary has column names as keys and corresponding values.
        Raises:
            ValueError: If the query is not a SELECT statement (does not start with "SELECT")
            RuntimeError: If the database connection fails or query execution encounters an error
        Example:
            >>> db_url = "sqlite:///example.db"
            >>> query = "SELECT id, name FROM users WHERE age > 18"
            >>> results = run_query(db_url, query)
            >>> print(results)
            [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]
        Note:
            - The function automatically closes the database connection after execution
            - Query results are converted to dictionaries for easy manipulation
            - Only read operations are permitted for security purposes
    """
    # Ensure only SELECT statements are allowed    
    if not query.strip().upper().startswith("SELECT"):
        raise ValueError("This function only supports SELECT queries for data retrieval.")

    try:
        engine = create_engine(db_connection_url, echo=False)
        with engine.connect() as conn:
            result = conn.execute(text(f"{query}"))
            rows = [dict(row._mapping) for row in result.fetchall()]

            conn.close()

            return rows
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database query failed: {e}")
