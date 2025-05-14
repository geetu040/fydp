import mysql.connector
from mysql.connector.cursor import MySQLCursor

def describe_sql(db_connection: MySQLCursor) -> str:
    """
    Retrieves and returns a human-readable schema description of all tables
    in the connected MySQL database.

    Parameters:
        db_connection (MySQLCursor): An active cursor connected to a MySQL database.

    Returns:
        str: A detailed string representation of the schema of each table,
             including table names and column definitions.
    """
    schema_str = ""

    db_connection.execute("SHOW TABLES;")
    tables = db_connection.fetchall()

    for (table_name,) in tables:
        schema_str += f"Schema for table: {table_name}\n"
        db_connection.execute(f"DESCRIBE `{table_name}`;")
        columns = db_connection.fetchall()
        for column in columns:
            # DESCRIBE returns: Field, Type, Null, Key, Default, Extra
            schema_str += f"  Column: {column[0]}, Type: {column[1]}, Nullable: {column[2]}, Key: {column[3]}, Default: {column[4]}, Extra: {column[5]}\n"
        schema_str += "\n"

    return schema_str
