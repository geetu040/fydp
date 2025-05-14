from . import (
	connect_sql,
	describe_sql,
	generate_sql,
	parse_response,
	execute_sql_query,
	create_data_response,
	extract_sql_credentials,
	select_sql_db,
)

def pipeline(user_query: str):
	# Step 1: Extract credentials from user query
	creds_list = extract_sql_credentials(user_query)
	if not creds_list:
		return "No valid database credentials found in your message. Please include host, database, user, password, and port."

	# Step 2: Connect to all databases and describe schema
	db_connections = []
	db_schemas = []
	db_info_map = {}  # maps schema to (connection, cursor, db info)

	for creds in creds_list:
		try:
			conn = connect_sql(
				host=creds['host'],
				database=creds['database'],
				user=creds['username'],
				password=creds['password'],
				port=int(creds.get('port', 3306)),
				sql_script=""  # No script at connection
			)
			schema = describe_sql(conn)
			db_connections.append(conn)
			db_schemas.append(schema)
			db_info_map[schema] = (conn, creds)
		except Exception as e:
			print(f"Failed to connect or describe schema: {e}")

	if not db_schemas:
		return "Failed to connect to any of the provided databases."

	# Step 3: Select relevant schemas
	relevant_schemas = select_sql_db(user_query, db_schemas)
	if not relevant_schemas:
		return "None of the databases seem relevant to your question."

	# Step 4: Generate SQL, execute it, and build response
	final_results = []
	for schema in relevant_schemas:
		conn, creds = db_info_map[schema]
		try:
			gen_sql_resp = generate_sql(user_query, schema)
			clean_sql = parse_response(gen_sql_resp)
			if not clean_sql:
				continue
			result = execute_sql_query(clean_sql, conn)
			if result:
				final_results.append((result, creds['database']))
		except Exception as e:
			print(f"Failed processing for DB {creds['database']}: {e}")

	if not final_results:
		return "No results were found for your query in the relevant databases."

	# Step 5: Combine results and respond
	responses = []
	for result, db_name in final_results:
		resp = create_data_response(user_query, result)
		responses.append(f"Results from `{db_name}`:\n{resp}")

	return "\n\n".join(responses)
