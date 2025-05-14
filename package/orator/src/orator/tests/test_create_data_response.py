import unittest
from orator import create_data_response

class TestCreateDataResponse(unittest.TestCase):
    def test_response_generation(self):
        user_query = "Who is in the table?"
        data = [(1, "Alice"), (2, "Bob")]
        response = create_data_response(user_query, data)
        self.assertTrue(any(name in response for name in ["Alice", "Bob"]))
