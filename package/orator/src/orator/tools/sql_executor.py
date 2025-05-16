import sqlite3
from typing import List, Tuple

def execute_sql_query(sql_query: str, db_connection: sqlite3.Cursor) -> List[Tuple]:
    """
    Executes a SQL query and fetches all results.

    Args:
        sql_query (str): SQL query string.
        db_connection (sqlite3.Cursor): SQLite cursor connected to the database.

    Returns:
        List[Tuple]: List of rows returned by the query.
    """
    db_connection.execute(sql_query)
    return db_connection.fetchall()
