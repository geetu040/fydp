from openai import OpenAI

client = OpenAI()

def create_data_response(user_query, data, relevant_docs=None):
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
