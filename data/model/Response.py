class Response:

    def __init__(self, status: bool, response=None):
        self.response = response
        self.response_status: bool = status

    def get_formatted_response(self):
        return self.__dict__
