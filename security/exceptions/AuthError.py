class AuthError(Exception):
    """
    Custom Auth exception for when the user fails authentication.
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
