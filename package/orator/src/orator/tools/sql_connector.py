import sqlite3

def connect_sql(db_path: str) -> sqlite3.Cursor:
    """
    Connects to an in-memory SQLite database and executes SQL script from a file.

    Args:
        db_path (str): Path to the SQL file containing schema and data.

    Returns:
        sqlite3.Cursor: Cursor object for executing further SQL commands.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    with open(db_path, "r") as f:
        sql_script = f.read()

    cursor.executescript(sql_script)
    return cursor
