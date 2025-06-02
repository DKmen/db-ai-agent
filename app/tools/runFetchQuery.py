from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict
from sqlalchemy import text

from app.db import engine

def run_query(query: str) -> List[Dict]:
    print(f"Running query: {query}")
    # Ensure only SELECT statements are allowed
    if not query.strip().upper().startswith("SELECT"):
        raise ValueError("This function only supports SELECT queries for data retrieval.")

    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"{query}"))
            rows = [dict(row._mapping) for row in result.fetchall()]

            conn.close()

            return rows
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database query failed: {e}")
