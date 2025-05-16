from tqdm import tqdm
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from . import connect_sql

def get_vector_store(rag_path):
	vector_store = InMemoryVectorStore.load(rag_path, OpenAIEmbeddings())
	return vector_store

def get_relevant_docs(vector_store, query):
	results = vector_store.similarity_search("apple iphone 11", k=3)
	results = [result.page_content[:200] for result in results]
	return results

def stringify_row(columns, row):
    return ", ".join(f"{col}={val}" for col, val in zip(columns, row))

def convert_to_vectors(db_path, rag_config={}):
	conn = connect_sql(db_path)
	documents = []
	for table, columns in rag_config.get("heirarchy", {}).items():
		columns_str = ", ".join(columns)
		conn.execute(f"SELECT {columns_str} FROM {table}")
		data = conn.fetchall()
		for row in tqdm(data):
			document = stringify_row(columns, row)
			document = Document(document)
			documents.append(document)

	gap = rag_config.get("gap", 50)
	vector_store = InMemoryVectorStore(OpenAIEmbeddings())

	for i in tqdm(range(0, len(documents), gap)):
		vector_store.add_documents(documents[i:i+gap])

	return vector_store

