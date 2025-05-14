
def execute_sql_query(sql_query, db_connection):
    db_connection.execute(sql_query)
    return db_connection.fetchall()
