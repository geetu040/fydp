import sqlite3

def connect_sql(db_path):
	conn = sqlite3.connect(":memory:")
	cursor = conn.cursor()

	with open(db_path, "r") as f:
		sql_script = f.read()

	cursor.executescript(sql_script)
	return cursor
