from enum import Enum


class ResponseStatusCode(Enum):
    SUCCESS = "200"
    SUCCESS_CREATE = "201"
    ERROR_CLIENT_REQUEST = "400"
    ERROR_UNAUTHENTICATED = "401"
    ERROR_UNAUTHORIZED = "403"
    ERROR_NOT_FOUND = "404"
    ERROR_INTERNAL = "500"
