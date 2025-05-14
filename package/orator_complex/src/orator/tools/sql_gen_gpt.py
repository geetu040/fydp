from openai import OpenAI
import os

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=OPENAI_API_KEY)

input_prompt_template = '''Task Overview:
You are a data science expert. Below, you are provided with a database schema and a natural language question. Your task is to understand the schema and generate a valid SQL query to answer the question.

Database Engine:
{db_engine}

Database Schema:
{db_details}
This schema describes the database's structure, including tables, columns, primary keys, foreign keys, and any relevant relationships or constraints.

Question:
{question}

Instructions:
- Make sure you only output the information that is asked in the question. If the question asks for a specific column, make sure to only include that column in the SELECT clause, nothing more.
- The generated query should return all of the information asked in the question without any missing or extra information.
- Before generating the final SQL query, please think through the steps of how to write the query.

Output Format:
In your answer, please enclose the generated SQL query in a code block:
```sql
-- Your SQL query
```
'''

def generate_sql(user_query: str, db_schema: str) -> str:
    """
    Generates a SQL query from a natural language question using the provided database schema.
    Parameters:
        user_query (str): The question or command in natural language.
        db_schema (str): A string describing the structure of the database (tables, columns, keys).

    Returns:
        str: The AI-generated SQL query in a code block format.
    """
    prompt = input_prompt_template.format(
        db_engine = "MySQL",
        db_details = db_schema,
        question = user_query,
    )
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You translate natural language to SQL using the given schema."},
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content
