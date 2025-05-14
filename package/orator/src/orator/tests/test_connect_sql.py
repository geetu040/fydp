import unittest
from orator import connect_sql

class TestConnectSQL(unittest.TestCase):
    def test_connect_sql_executes_script(self):
        cursor = connect_sql("tests/test_schema.sql")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test';")
        self.assertEqual(cursor.fetchone()[0], 'test')
