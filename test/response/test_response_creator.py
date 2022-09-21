import os
from unittest import TestCase

from response.ResponseCreator import ResponseCreator


# class TestObject:
#
#     def __init__(self):
#         self.message = "hello"


test_response_object = {
    "message": "hello"
}


class TestResponseCreator(TestCase):
    def test_success_response(self):
        os.environ['stage'] = "BETA"
        testee = ResponseCreator(test_response_object)
        result = testee.generate_successful_response()

        self.assertEqual(result['body']['message'], "hello")
        self.assertEqual(result['statusCode'], '200')
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
