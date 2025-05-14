import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

input_prompt_template = '''Task Overview:
You are a data science expert. Below, you are provided with a database schema and a natural language question. Your task is to understand the schema and generate a valid SQL query to answer the question.

Database Engine:
SQLite

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
```
-- Your SQL query
```

Take a deep breath and think step by step to find the correct SQL query.'''

model_path = "geetu040/tuned_sql_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    quantization_config=bnb_config,
).to("cuda:0")

def generate_sql(user_query, schema):
	prompt = input_prompt_template.format(db_details=schema, question=user_query)
	chat_prompt = tokenizer.apply_chat_template(
		[{"role": "user", "content": prompt}],
		add_generation_prompt = True, tokenize = False
	)

	inputs = tokenizer([chat_prompt], return_tensors="pt")
	inputs = inputs.to(model.device)

	output_ids = model.generate(
		**inputs,
		eos_token_id = tokenizer.eos_token_id,
		max_new_tokens = 2048
	)

	input_len = len(inputs.input_ids[0])
	output_ids = output_ids[0][input_len:]

	response = tokenizer.batch_decode([output_ids], skip_special_tokens = True)[0]
	return response
