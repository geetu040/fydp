from orator.database import Database
from langchain_community.utilities.sql_database import SQLDatabase as LangchainSQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain import hub
from langgraph.prebuilt import create_react_agent

class SQLDatabase(Database):
	def __init__(self, db):
		self.db = db

	def create_agent(self, llm):
		toolkit = SQLDatabaseToolkit(db=self.db, llm=llm)
		prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
		system_message = prompt_template.format(dialect="SQLite", top_k=5)
		agent = create_react_agent(llm, toolkit.get_tools(), prompt=system_message)
		return agent

	def process_message(self, message):
		return {"messages": [("user", message)]}

	def postprocess(self, response):
		return response['messages'][-1].content

	@classmethod
	def from_uri(cls, database_uri, engine_args=None, **kwargs):
		db = LangchainSQLDatabase.from_uri(database_uri, engine_args, **kwargs)
		return cls(db)

__all__ = ["SQLDatabase"]
