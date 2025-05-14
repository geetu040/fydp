from langchain.agents import initialize_agent, Tool, AgentType
from langchain.agents import AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.callbacks import StreamlitCallbackHandler

from . import (
    connect_sql,
    describe_sql,
    generate_sql,
    parse_response,
    execute_sql_query,
    create_data_response,
    extract_sql_credentials,
    select_sql_db
)


tools = [
    Tool(
        name="extract_sql_credentials",
        func=extract_sql_credentials,
        description="Extracts SQL credentials from the user's query"
    ),
    Tool(
        name="connect_sql",
        func=connect_sql,
        description="Establishes a connection to a SQL database"
    ),
    Tool(
        name="describe_sql",
        func=describe_sql,
        description="Describes the schema of the SQL database"
    ),
    Tool(
        name="select_sql_db",
        func=select_sql_db,
        description="Selects the most relevant databases based on the user query"
    ),
    Tool(
        name="generate_sql",
        func=generate_sql,
        description="Generates a SQL query from the user's question and schema"
    ),
    Tool(
        name="parse_response",
        func=parse_response,
        description="Parses the generated SQL query"
    ),
    Tool(
        name="execute_sql_query",
        func=execute_sql_query,
        description="Executes the SQL query in the database"
    ),
    Tool(
        name="create_data_response",
        func=create_data_response,
        description="Creates a natural language response from the SQL query results"
    ),
]


llm = OpenAI(temperature=0, streaming=True)


callback_handler = StreamlitCallbackHandler()


agent_executor = AgentExecutor(
    tools=tools,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    llm=llm,
    callbacks=[callback_handler],  
    verbose=True
)


def pipeline(messages):
    conversation = "\n".join([message["content"] for message in messages])
    response = agent_executor.stream(conversation)
    return response 
