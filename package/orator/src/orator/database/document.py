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

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
import json
from langchain_core.messages import SystemMessage, HumanMessage

from langchain.schema import SystemMessage, HumanMessage
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough

class DocumentDatabase(Database):
	def __init__(
			self,
			path: str,
			model_name: str = "sentence-transformers/all-mpnet-base-v2",
			top_k: int = 3,
			model_kwargs = None,
			encode_kwargs = None,
		):
		self.path = path
		self.model_name = model_name
		self.top_k = top_k
		self.model_kwargs = {"device": "cpu"} if model_kwargs is None else model_kwargs
		self.encode_kwargs = {"batch_size": 8} if encode_kwargs is None else encode_kwargs

		embeddings = HuggingFaceEmbeddings(
			model_name=self.model_name,
			model_kwargs=self.model_kwargs,
			encode_kwargs=self.encode_kwargs,
			show_progress=False,
		)
		self.vector_store = InMemoryVectorStore(embeddings)
		with open(path, 'rb') as f:
			self.vector_store.store = json.load(f)

	def create_agent(self, llm):
		# Step 1: Retrieve relevant documents from the vector store
		retrieve_docs = RunnableLambda(lambda message: (message, self.vector_store.similarity_search(message, k=self.top_k)))

		# Step 2: Format the retrieved docs into a prompt
		def format_prompt(inputs):
			message, docs = inputs
			prompt = [
				SystemMessage(
					"You are an assistant for question-answering tasks. "
					"Use the following pieces of retrieved context to answer "
					"the question. If you don't know the answer, say that you "
					"don't know. Use three sentences maximum and keep the "
					"answer concise."
					"\n\n"
					f"{'\n\n'.join(doc.page_content for doc in docs)}"
				),
				HumanMessage(message)
			]
			return prompt

		format_prompt_node = RunnableLambda(format_prompt)

		# Step 3: Invoke LLM with the formatted prompt
		invoke_llm = llm

		# Step 4: Chain everything together
		agent_pipeline = RunnablePassthrough() | retrieve_docs | format_prompt_node | invoke_llm

		return agent_pipeline

	def process_message(self, message):
		return message

	def postprocess(self, response):
		return response.content

__all__ = ["SQLDatabase"]
