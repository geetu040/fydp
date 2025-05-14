import unittest
from orator import connect_sql, execute_sql_query

class TestExecuteSQLQuery(unittest.TestCase):
    def test_query_returns_expected_data(self):
        cursor = connect_sql("tests/test_schema.sql")
        result = execute_sql_query("SELECT name FROM test WHERE id = 1;", cursor)
        self.assertEqual(result, [('Alice',)])
