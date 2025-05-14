
def describe_sql(db_connection):
	schema_str = ""

	db_connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tables = db_connection.fetchall()

	for table_name in tables:
		schema_str += f"Schema for table: {table_name[0]}\n"
		db_connection.execute(f"PRAGMA table_info({table_name[0]});")
		for column in db_connection.fetchall():
			schema_str += f"  {column}\n"
		schema_str += "\n"
	
	return schema_str
