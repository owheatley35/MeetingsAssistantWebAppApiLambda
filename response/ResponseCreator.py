import os

from Constants import ALLOWED_ORIGINS
from response.ResponseStatusCode import ResponseStatusCode
from response.ResponseType import ResponseType


def form_response(status_code: ResponseStatusCode, content_type: ResponseType, response_body: dict) -> object:

    stage: str = os.environ["stage"]
    origin: str = ALLOWED_ORIGINS.get(stage)

    return {
        "statusCode": status_code.value,
        "headers": {
            "Content-Type": content_type.value,
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": origin
        },
        "body": response_body
    }


class ResponseCreator:

    def __init__(self, body: object):
        self._body = body

    def generate_successful_response(self):
        return form_response(ResponseStatusCode.SUCCESS, ResponseType.JSON, self._body)

    def generate_failure_response(self):
        return form_response(ResponseStatusCode.ERROR_INTERNAL, ResponseType.JSON, self._body)
