import unittest
from orator import connect_sql, describe_sql

class TestDescribeSQL(unittest.TestCase):
    def test_describe_sql_structure(self):
        cursor = connect_sql("tests/test_schema.sql")
        schema = describe_sql(cursor)
        self.assertIn("Schema for table: test", schema)
        self.assertIn("id", schema)
        self.assertIn("name", schema)
