import mysql.connector
from mysql.connector.cursor import MySQLCursor

CONNECTIONS = {}

def connect_sql(
	host: str,
	database: str,
	user: str,
	password: str,
	port: int,
	sql_script: str
) -> MySQLCursor:
	"""
	Establishes a connection to a MySQL database server and executes a given SQL script.

	Parameters:
		host (str): The hostname or IP address of the MySQL server.
		database (str): The name of the database to connect to.
		user (str): The username used for authentication.
		password (str): The password used for authentication.
		port (int): The port number of the MySQL server.
		sql_script (str): A string containing one or more SQL statements separated by semicolons.

	Returns:
		MySQLCursor: A cursor object after executing the SQL script.
	"""
	
	key = host + database + user + password + str(port)
	if key in CONNECTIONS:
		return CONNECTIONS[key]
	
	conn = mysql.connector.connect(
		host=host,
		database=database,
		user=user,
		password=password,
		port=port
	)
	cursor = conn.cursor()

	for statement in sql_script.split(';'):
		stmt = statement.strip()
		if stmt:
			cursor.execute(stmt)

	conn.commit()

	CONNECTIONS[key] = cursor

	return cursor
