from orator.database import Database
from langchain_community.utilities.sql_database import SQLDatabase as LangchainSQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain import hub

from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.schema import SystemMessage
from langchain.prompts import PromptTemplate
import pandas as pd
from langchain.output_parsers import RegexParser

class CSVDatabase(Database):
	def __init__(self, path):
		self.path = path
		self.df = pd.read_csv(path)
		self.df_info = self.get_data_info()

	def get_data_info(self):
		schema = self.df.dtypes.to_dict()
		sample_data = self.df.sample(3, random_state=42).to_dict(orient='records')  # Adjust sample size as needed
		space = "\n\n"
		return (
			"This data is stored in pandas dataframe as `df`." +
			space +
			"It has the following schema:\n" +
			str(schema) +
			space +
			"Here are a few examples from the `df`:\n" +
			str(sample_data)
		)

	def create_agent(self, llm):

		message = "what is the most expensive item?"
		response = llm.invoke(
			(
				"User has asked the following question:\n\n"
				f"{message}\n\n"
				"The data is available in a pandas dataframe `df`. "
				"Here is some description from the `df`:\n"
				f"{self.df_info}\n\n"
				"Now output ONLY a single valid query that can be executed using `df.query(query)`."
				"Output format: ```query\n<query>\n```"
			)
		).content
		print(response)
		response = RegexParser(regex=r"```(?:query)?\n(.*?)\n```", output_keys=["query"]).parse(response)
		print(response)
		exit()

		def query_dataframe(query):
			try:
				return self.df.query(query).to_dict(orient="records")
			except Exception as e:
				return str(e)

		tools = [
			Tool(
				name="QueryDataFrame",
				func=query_dataframe,
				description="Use this tool to query the dataframe using pandas syntax."
			)
		]

		system_prompt = PromptTemplate(
			input_variables=["tools", "agent_scratchpad", "tool_names"],
			template=(
				"You are a helpful AI assistant. You have access to the following tools:\n\n{tools}\n\n"
				"When responding, use ONLY the available tools. The tool names are: {tool_names}.\n\n"
				"Follow this format strictly:\n"
				"- Thought: Think step-by-step.\n"
				"- Action: Call a tool. Example: `Action: tool_name(argument)`\n"
				"- Observation: The result from the tool.\n\n"
				"You must NEVER ask the user for clarification. Instead, use the tools to gather data."
				"Here is your scratchpad:\n\n{agent_scratchpad}"
			)
		)

		agent = create_react_agent(llm, tools, prompt=system_prompt)
		agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
		return agent_executor

	def process_message(self, message):
		return {"messages": [("user", message)]}

	def postprocess(self, response):
		return response['messages'][-1].content

__all__ = ["SQLDatabase"]
