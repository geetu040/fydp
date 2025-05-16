from openai import OpenAI
from typing import List, Optional, Tuple, Any

client = OpenAI()

def create_data_response(user_query: str, data: Any, relevant_docs: Optional[List[str]] = None) -> str:
    """
    Creates a natural language response from SQL data and optional relevant documents.

    Args:
        user_query (str): The original question from the user.
        data (Any): Data returned from the database.
        relevant_docs (Optional[List[str]]): List of related documents for RAG.

    Returns:
        str: A generated response string in natural language.
    """
    data = str(data)[:1000]
    relevant_docs = "\n".join(relevant_docs) if relevant_docs is not None else ""

    prompt = f"""You are a data assistant. The user asked the following question:

    "{user_query}"

    Here is the data returned from the database (as a Python list of rows):
    {data}

    Here are some relevant documents that may help in answering the question:
    {relevant_docs}

    Please generate a clear and concise response in plain English based on this data.
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You summarize data for user questions."},
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content.strip()
