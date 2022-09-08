import logging

LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class LoggingHelper:
    """
    Class to create a logger configured for a class.
    """
    def __init__(self, class_name: str):
        """
        :param class_name Name of the class to log to.
        """
        self._logger = logging.getLogger(class_name)
        self._logger.setLevel(logging.INFO)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
        self._logger.addHandler(stream_handler)

    def retrieve_logger(self) -> logging.Logger:
        """
        Retrieve the logger.
        """
        return self._logger
