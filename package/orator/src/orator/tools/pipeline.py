from . import (
	connect_sql,
	describe_sql,
	parse_response,
	execute_sql_query,
	create_data_response,
)
from .sql_gen_gpt import generate_sql

def pipeline(user_query, db_paths):

	db_conns = [connect_sql(i) for i in db_paths]
	db_descs = [describe_sql(i) for i in db_conns]
	response = generate_sql(user_query, db_descs[0])
	sql_query = parse_response(response)
	data = execute_sql_query(sql_query, db_conns[0])
	response = create_data_response(user_query, data)

	return response
