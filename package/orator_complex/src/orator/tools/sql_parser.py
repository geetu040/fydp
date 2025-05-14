import re

def parse_response(response_text: str) -> str:
    """
    Extracts the final SQL query from a response string containing one or more SQL code blocks.

    Parameters:
        response_text (str): The full text response, typically returned by an LLM,
                             which may contain SQL queries enclosed in triple backticks.

    Returns:
        str: The last SQL query found in the response, cleaned of extra whitespace.
             Returns an empty string if no SQL code block is found.
    """
    # Regex pattern to match code blocks that start with ```sql and end with ```
    sql_block_pattern = r"```sql\s*(.*?)\s*```"

    # Find all SQL code blocks in the response using DOTALL to match across newlines
    sql_blocks = re.findall(sql_block_pattern, response_text, re.DOTALL)

    if sql_blocks:
        # Return the last SQL query found, after trimming any surrounding whitespace
        return sql_blocks[-1].strip()
    else:
        # No SQL code block found in the response
        return ""
