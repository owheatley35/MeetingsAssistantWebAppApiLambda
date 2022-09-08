import json
from logging import Logger
from boto3 import Session
from helper.BotoHelper import global_boto_session

import Constants
from helper.LoggingHelper import LoggingHelper


class SecretProvider:
    """
    Class to provide a secret object from a given secret name.
    """

    def __init__(self, boto_session=global_boto_session, logger=LoggingHelper(__name__).retrieve_logger()):
        self._logger = logger

        logger.info("Retrieving secrets client.")

        self._secrets_manager_client = boto_session.client(
            service_name=Constants.SECRETS_CLIENT_NAME,
            region_name=Constants.REGION
        )

        logger.info("Secrets Client Retrieved.")

    def retrieve_secret(self, secret_name: str):
        """
        Retrieves Secret from AWS Secrets Manager from secret name.

        :param secret_name string name of the secret

        :return: Object containing the secret in a key pair fashion
        """
        try:
            secret = self._secrets_manager_client.get_secret_value(
                SecretId=secret_name
            )
            self._logger.info("Secret Retrieved")
            return json.loads(secret)
        except Exception as e:
            self._logger.error("Failed to retrieve secret.")
            self._logger.error(e)
