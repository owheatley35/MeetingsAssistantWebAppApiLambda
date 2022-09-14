from unittest import TestCase

successful_case_event = {
    "header": {
        "header_1": "header_1"
    },
    "requestContext": {
        "http": {
            "path": "/path"
        }
    },
    "queryStringParameters": {
        "param1": "param1_value"
    }
}

empty_case_event = {}


class LambdaEventTest(TestCase):

    def test_lambda_event(self):
        self.assertTrue(False)
