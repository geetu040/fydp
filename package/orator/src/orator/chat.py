from orator import (
	connect_sql,
	describe_sql,
	parse_response,
	execute_sql_query,
	create_data_response,
	get_vector_store,
	get_relevant_docs,
)

class Chatbot:
	def __init__(self, db_path, rag_path=None, use_custom_model=False):
		self.db_path = db_path
		self.rag_path = rag_path
		self.use_custom_model = use_custom_model

		self.conn = connect_sql(self.db_path)
		self.schema = describe_sql(self.conn)
		self.vector_store = get_vector_store(rag_path) if rag_path else None

		if self.use_custom_model:
			from orator.tools.sql_gen_custom import generate_sql
		else:
			from orator.tools.sql_gen_gpt import generate_sql
		self.generate_sql = generate_sql

	def add_vector_store(self, vector_store):
		self.vector_store = vector_store

	def answer(self, prompt: str) -> str:
		"""
		Generate a response to the given prompt.
		"""
		sql_response = self.generate_sql(prompt, self.schema)
		sql_query = parse_response(sql_response)
		print(f"SQL Query: {sql_query}")
		sql_data = execute_sql_query(sql_query, self.conn)
		print(f"SQL Data: {sql_data}")

		relevant_docs = None
		if self.vector_store:
			relevant_docs = get_relevant_docs(self.vector_store, prompt)
		print(f"Relevant Docs: {relevant_docs}")

		response = create_data_response(prompt, sql_data, relevant_docs)
		return response, {"sql_query": sql_query, "sql_data": sql_data, "relevant_docs": relevant_docs}
