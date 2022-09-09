import sys

from data.provider.SecretProvider import SecretProvider
from database.DBConfiguration import DBConfiguration
from helper.LoggingHelper import LoggingHelper
import os


class DBConfigurationProvider:
    """
    Retrieves Database configuration details from AWS Secrets Manager for access from AWS services and provides that data.
    """

    def __init__(self, secrets_provider=SecretProvider(), logger=LoggingHelper(__name__).retrieve_logger()):
        try:
            logger.info("Retrieving env data")
            db_credentials_secret_name = os.environ['databaseInformationSecretName']
            logger.info("Retrieving Secret Value...")
            db_credentials = secrets_provider.retrieve_secret(db_credentials_secret_name)
        except Exception as e:
            logger.error(e)
            sys.exit()

        logger.info("Accessing Data...")
        self._host = db_credentials['host']
        self._db_username = db_credentials['username']
        self._db_password = db_credentials['password']
        self._database_identifier = db_credentials['dbInstanceIdentifier']
        self._db_port = int(db_credentials['port'])
        logger.info("Data Access Complete.")

    def get_configuration(self) -> DBConfiguration:
        """
        :return: DBConfiguration object containing all the information required to create a connection to a database.
        """
        return DBConfiguration(self._host, self._db_username, self._db_password, self._db_port, self._database_identifier)
