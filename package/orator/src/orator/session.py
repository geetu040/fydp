from orator.sql_generation import generate_sql_query
from orator.sql_parsing import parse_sql_query
from orator.sql_validation import validate_sql_query
from orator.sql_execution import execute_sql_query
from orator.sql_db_selection import select_sql_db
import psycopg2
from psycopg2 import OperationalError

# Shared global (should be thread-safe or scoped appropriately in production)
DB_CONNECTIONS = {}

# Dummy schemas and DB connections; replace with real ones
DB_SCHEMAS = {
    "priceoye": "Latest mobile phones",
    "daraz": "All kinds of products",
    "mega": "Electronics (laptops, mobile phones, headphones)"
}


def create_db_connection(name, server, username, password, port, database="postgres"):
    """
    Attempts to create a DB connection with the given credentials.
    If successful, stores it in DB_CONNECTIONS under the provided name.
    
    Returns:
        str: Success or failure message
    """
    try:
        conn = psycopg2.connect(
            host=server,
            user=username,
            password=password,
            port=port,
            dbname=database,
            connect_timeout=5
        )
        DB_CONNECTIONS[name] = conn
        return f"Connected to {name} successfully."
    except OperationalError as e:
        return f"Connection to {name} failed: {str(e)}"



class Session:
    def __init__(self):
        self.chat_history = []

    def chat(self, messages, stream_mode=None):
        user_prompt = messages[-1]["content"]  # Last user message
        self.chat_history.extend(messages)

        # Step 1: Pick most relevant DBs
        schema_names = list(DB_SCHEMAS.keys())
        sorted_dbs = select_sql_db(user_prompt, [DB_SCHEMAS[s] for s in schema_names])
        best_db = schema_names[[DB_SCHEMAS[s] for s in schema_names].index(sorted_dbs[0])]

        # Step 2: Generate SQL using LLM
        sql_schema = DB_SCHEMAS[best_db]
        model_output = generate_sql_query(user_prompt, sql_schema)

        # Step 3: Parse query
        sql_query = parse_sql_query(model_output)
        if not sql_query:
            return "Could not generate a valid SQL query."

        # Step 4: Validate query
        if not validate_sql_query(sql_query):
            return "The generated SQL query is invalid."

        # Step 5: Execute query
        db_conn = DB_CONNECTIONS[best_db]
        result = execute_sql_query(sql_query, db_conn)

        # Stream if required
        if stream_mode == "text":
            for chunk in self._stream_response(result):
                yield chunk
        else:
            return result

    def _stream_response(self, result):
        """Yields text in chunks for streaming purposes."""
        if isinstance(result, dict) and "error" in result:
            yield f"Error: {result['error']}"
        elif isinstance(result, list):
            yield "Results:\n"
            for row in result:
                yield str(row) + "\n"
        else:
            yield str(result)


__all__ = ["Session"]
