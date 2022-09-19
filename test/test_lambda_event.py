from unittest import TestCase
from lambda_event import LambdaEvent
from security.exceptions.InvalidHeaderException import InvalidHeaderException


header = {"header_1": "header_1"}
path = "/get/meeting"
parameters = {"param_1": "param_1"}

successful_case_event = {
    "header": header,
    "requestContext": {
        "http": {
            "path": path
        }
    },
    "queryStringParameters": parameters
}

empty_case_event = {}


class LambdaEventTest(TestCase):

    def test_lambda_event(self):
        test_event = LambdaEvent(successful_case_event)

        self.assertEqual(test_event.get_header(), header)
        self.assertEqual(test_event.get_request_path(), path)
        self.assertEqual(test_event.get_query_parameters(), parameters)

    def test_lambda_event_empty(self):
        self.assertRaises(InvalidHeaderException, LambdaEvent, empty_case_event)
