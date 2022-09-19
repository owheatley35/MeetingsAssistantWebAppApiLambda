from enum import Enum

from response.ResponseCreator import form_response
from response.ResponseStatusCode import ResponseStatusCode
from response.ResponseType import ResponseType


class SetResponses(Enum):
    UNAUTHENTICATED = form_response(ResponseStatusCode.ERROR_UNAUTHENTICATED, ResponseType.JSON, {"message": "Unauthenticated Request"})
    BLANK_SUCCESS = form_response(ResponseStatusCode.SUCCESS, ResponseType.JSON, {})
    UNAUTHORIZED = form_response(ResponseStatusCode.ERROR_UNAUTHORIZED, ResponseType.JSON, {"message": "User not authorized to access this endpoint."})
    INVALID_ROUTE = form_response(ResponseStatusCode.ERROR_NOT_FOUND, ResponseType.JSON, {"message": "Invalid route."})
    INVALID_REQUEST = form_response(ResponseStatusCode.ERROR_CLIENT_REQUEST, ResponseType.JSON, {"message": "Invalid request."})
    INTERNAL_ERROR = form_response(ResponseStatusCode.ERROR_INTERNAL, ResponseType.JSON, {})
