from openai import OpenAI
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def create_data_response(user_query, data):
    prompt = f"""You are a data assistant. The user asked the following question:
    
    "{user_query}"

    Here is the data returned from the database (as a Python list of rows):
    {data}

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
