from mysql.connector.cursor import MySQLCursor
from typing import List, Any

def execute_sql_query(sql_query: str, db_cursor: MySQLCursor) -> List[Any]:
    """
    Executes a given SQL query using a MySQL database cursor.

    Parameters:
        sql_query (str): The SQL query string to be executed.
        db_cursor (MySQLCursor): An active cursor connected to a MySQL database.

    Returns:
        List[Any]: The fetched result rows if the query returns data (e.g., SELECT).
                   Returns an empty list for queries that don't return results.
    """
    db_cursor.execute(sql_query)

    # Return fetched results only if the query produces output
    if db_cursor.description:
        return db_cursor.fetchall()
    else:
        return []
