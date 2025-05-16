
# Setting Up

```bash
pip install -r requirements.txt
pip install -e .
```

# Usage

### Simple QA Using SQL Database

```py
from orator import Chatbot

db_path = "path to your database file"

chat = Chatbot(db_path=db_path)

response, meta = chat.answer(
	# "tell me about the apple phones in the database"
	# "what does the data look like?"
	# "which is the largest table in the database?"
	"how many columns are in each table of the database?"
)
print(response)

```

### Query using SQL Database and Vector Store

```py
from orator import convert_to_vectors

db_path = "path to your database file"

vector_store = convert_to_vectors(
	db_path=db_path,
	rag_config={
		"heirarchy": {
			"data": ["id", "slug", "title", "brand", "category", "vendor", "used", "address", "original_price", "discounted_price", "specifications", "description"],
		},
	},
)

# you can save and use the vector store later
# dump_path = vector_store.dump("path to your dump file")
# chat = Chatbot(db_path=db_path, rag_path=dump_path)

chat = Chatbot(db_path=db_path)
chat.add_vector_store(vector_store)

response, meta = chat.answer(
	# "tell me about the apple phones in the database"
	# "what does the data look like?"
	# "which is the largest table in the database?"
	"how many columns are in each table of the database?"
)
print(response)
```
