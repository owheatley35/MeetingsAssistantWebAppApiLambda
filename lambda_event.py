from security.exceptions.InvalidHeaderException import InvalidHeaderException


class LambdaEvent:
    """
    Class to model the relevant event information of a Lambda function.
    """
    def __init__(self, event):
        """
        :param event: event object from the Lambda function
        """
        self._event = event

        if "headers" in self._event and "path" in self._event and "queryStringParameters" in self._event:
            self._header = self._event["headers"]
            self._request_path = self._event["path"]
            self._query_parameters = self._event["queryStringParameters"]
        else:
            raise InvalidHeaderException("Invalid Event")

    def get_header(self) -> dict:
        """
        :return: dictionary containing the headers of the request
        """
        return self._header if self._header else {}

    def get_request_path(self) -> str:
        """
        :return: string containing the request path
        """
        return self._request_path

    def get_query_parameters(self) -> dict:
        """
        :return: dictionary containing the query parameters
        """
        return self._query_parameters if self._query_parameters else {}
