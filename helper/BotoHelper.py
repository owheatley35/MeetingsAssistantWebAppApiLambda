import boto3
from boto3 import Session


class BotoHelper:
    """
    Build a boto session.
    """

    def __init__(self):
        self._boto_session = boto3.session.Session()

    def retrieve_boto_session(self) -> Session:
        """
        Retrieve the boto session.

        :return: Boto3 Session
        """
        return self._boto_session


global_boto_session = BotoHelper().retrieve_boto_session()
