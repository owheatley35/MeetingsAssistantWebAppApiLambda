class LambdaEvent:
    """
    Class to model the relevant event information of a Lambda function.
    """
    def __init__(self, event):
        """
        :param event: event object from the Lambda function
        """
        self._event = event
        self._header = event["header"]
        self._request_path = event["requestContext"]["http"]["path"]
        self._query_parameters = event["queryStringParameters"]

    def get_header(self) -> dict:
        """
        :return: dictionary containing the headers of the request
        """
        return self._header

    def get_request_path(self) -> str:
        """
        :return: string containing the request path
        """
        return self._request_path

    def get_query_parameters(self) -> dict:
        """
        :return: dictionary containing the query parameters
        """
        return self._query_parameters
