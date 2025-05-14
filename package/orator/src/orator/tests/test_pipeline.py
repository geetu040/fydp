import unittest
from orator import pipeline

class TestPipeline(unittest.TestCase):
    def test_pipeline_end_to_end(self):
        response = pipeline("List all names", ["tests/test_schema.sql"])
        self.assertIn("Alice", response)
        self.assertIn("Bob", response)
