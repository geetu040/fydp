import re

def extract_sql_credentials(user_query):
	"""
	Extracts SQL credentials from a user query string.

	This function uses a regular expression to identify and extract
	SQL credentials such as username, password, host, and database name
	from the provided user query. The extracted credentials are returned
	as a dictionary.

	Parameters:
		user_query (str): The user query string containing SQL credentials.

	Returns:
		List[dict]: A list of dictionary containing the extracted SQL credentials.
			  Keys include 'username', 'password', 'host', and 'database'.
	"""
	pattern = r"Server:\s*(?P<host>[^\s]+)\s*Username:\s*(?P<username>[^\s]+)\s*Password:\s*(?P<password>[^\s]+)\s*Port:\s*(?P<port>\d+)"
	matches = re.findall(pattern, user_query)
	
	# Convert to list of dicts
	credentials = [
		{"host": m[0], "username": m[1], "password": m[2], "port": m[3]}
		for m in matches
	]
	return credentials
