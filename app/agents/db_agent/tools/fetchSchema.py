from typing import Dict, List, Optional
from pydantic import BaseModel
from sqlalchemy import text as Text

from sqlmodel import create_engine
from langchain_core.tools import tool

class Column(BaseModel):
    name: str
    type: str
    nullable: bool
    default: Optional[str]

class ForeignKey(BaseModel):
    column: str
    references: Dict[str, str]

class TableSchema(BaseModel):
    columns: List[Column]
    foreignKeys: List[ForeignKey]

class DatabaseSchema(BaseModel):
    schema_name: str
    tables: Dict[str, TableSchema]

@tool
def fetch_schema(db_connection_url: str) -> DatabaseSchema:
    """
    Fetch and construct a comprehensive database schema from a PostgreSQL database. This function connects to a PostgreSQL database and retrieves complete schema information including tables, columns, and foreign key relationships from the 'public' schema.
    
    Args:
        db_connection_url (str): The database connection URL in the format:
            'postgresql://username:password@host:port/database_name'
    Returns:
        DatabaseSchema: A structured object containing:
            - schema_name: The name of the schema (default: 'public')
            - tables: Dictionary mapping table names to TableSchema objects, where each
              TableSchema contains:
                - columns: List of Column objects with name, type, nullable, and default properties
                - foreignKeys: List of ForeignKey objects with column and reference information
    Raises:
        SQLAlchemyError: If there's an error connecting to the database or executing queries
        ValueError: If the connection URL is invalid or malformed
    Example:
        >>> schema = fetch_schema('postgresql://user:pass@localhost:5432/mydb')
        >>> print(schema.tables.keys())
        dict_keys(['users', 'orders', 'products'])
        >>> print(schema.tables['users'].columns[0].name)
        'id'
    Note:
        - Only retrieves tables from the 'public' schema
        - Only fetches BASE TABLE types (excludes views, temporary tables, etc.)
        - Foreign key relationships are captured with full reference details
    """
    schema = DatabaseSchema(schema_name="public", tables={})
    engine = create_engine(db_connection_url, echo=False)

    with engine.connect() as conn:
        # Step 1: Get all tables in public schema
        tables = conn.execute(Text(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """
        )).fetchall()

        for table in tables:
            table_name = table[0]
            schema.tables[table_name] = TableSchema(columns=[], foreignKeys=[])

            # Step 2: Get column metadata
            columns = conn.execute(Text(f"""
                SELECT
                  column_name,
                  data_type,
                  is_nullable,
                  column_default
                FROM information_schema.columns
                WHERE table_name = '{table_name}';
            """),{
                "table_name": table_name
            }).fetchall()

            schema.tables[table_name].columns = [
                Column(
                    name=col[0],
                    type=col[1],
                    nullable=(col[2] == 'YES'),
                    default=col[3]
                )
                for col in columns
            ]

            # Step 3: Get foreign key relationships
            fks = conn.execute(Text(f"""
                SELECT
                  kcu.column_name,
                  ccu.table_name AS foreign_table_name,
                  ccu.column_name AS foreign_column_name
                FROM
                  information_schema.table_constraints AS tc
                  JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                  JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                WHERE
                  tc.constraint_type = 'FOREIGN KEY'
                  AND tc.table_name = '{table_name}';
            """),{
                "table_name": table_name
            }).fetchall()

            schema.tables[table_name].foreignKeys = [
                ForeignKey(
                    column=fk[0],
                    references={"table": fk[1], "column": fk[2]}
                )
                for fk in fks
            ]

        conn.close()

    return schema
