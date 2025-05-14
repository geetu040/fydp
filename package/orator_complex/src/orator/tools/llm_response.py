from openai import OpenAI
from typing import Any, List
import os

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=OPENAI_API_KEY)

def create_data_response(user_query: str, data: List[Any]) -> str:
    """
    Generates a natural language summary of data returned from a database query.

    Parameters:
        user_query (str): The original question asked by the user.
        data (List[Any]): The result of the SQL query as a list of rows.

    Returns:
        str: A plain English response summarizing the key information from the data.
    """
    prompt = f"""
    You are a helpful data assistant. A user asked the following question:

    "{user_query}"

    Below is the data returned from the database query (formatted as a Python list of rows):
    {data}

    Please summarize the results clearly in plain English. Focus only on what the data shows in response to the user's question.
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You summarize database results into concise English answers."},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content.strip()
