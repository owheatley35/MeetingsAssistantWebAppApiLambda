from response.ResponseStatusCode import ResponseStatusCode
from response.ResponseType import ResponseType


def form_response(status_code: ResponseStatusCode, content_type: ResponseType, response_body: object) -> object:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": content_type
        },
        "body": response_body
    }


class ResponseCreator:

    def __init__(self, body: object):
        self._body = body

    def generate_successful_response(self):
        return form_response(ResponseStatusCode.SUCCESS, ResponseType.JSON, self._body)
