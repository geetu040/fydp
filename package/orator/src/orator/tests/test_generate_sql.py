import unittest
from orator import connect_sql, describe_sql
from orator.tools.sql_gen_gpt import generate_sql

class TestGenerateSQL(unittest.TestCase):
    def test_generate_sql_output_contains_sql(self):
        cursor = connect_sql("tests/test_schema.sql")
        schema = describe_sql(cursor)
        output = generate_sql("Get all names", schema)
        self.assertIn("SELECT", output.upper())
        self.assertIn("FROM", output.upper())
