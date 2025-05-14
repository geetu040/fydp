import unittest
from orator import parse_response

class TestParseResponse(unittest.TestCase):
    def test_parse_sql_block(self):
        response = "```sql\nSELECT * FROM test;\n```"
        sql = parse_response(response)
        self.assertEqual(sql, "SELECT * FROM test;")

    def test_parse_no_sql_block(self):
        response = "This is just plain text."
        sql = parse_response(response)
        self.assertEqual(sql, "")
