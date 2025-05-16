import re

def parse_response(response: str) -> str:
    """
    Parses a SQL response block from a text string.

    Args:
        response (str): Text containing SQL query enclosed in triple backticks.

    Returns:
        str: Parsed SQL query string or empty string if not found.
    """
    pattern = r"```sql\s*(.*?)\s*```"

    sql_blocks = re.findall(pattern, response, re.DOTALL)

    if sql_blocks:
        # Extract the last SQL query in the response text and remove extra whitespace characters
        last_sql = sql_blocks[-1].strip()
        return last_sql
    else:
        # print("No SQL blocks found.")
        return ""
