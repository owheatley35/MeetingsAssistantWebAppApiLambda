from data.provider.DBConfigurationProvider import DBConfigurationProvider
from database.DatabaseConnectionHelper import DatabaseConnectionHelper
from database.MySQLQueryExecutor import MySQLQueryExecutor


class DatabaseConnector:
    """
    Super Class of classes that need to make a database connection.
    """

    def __init__(self):
        db_config = DBConfigurationProvider().get_configuration()
        self._connection_helper = DatabaseConnectionHelper(db_config)
        self._query_helper = MySQLQueryExecutor(self._connection_helper.get_connection_cursor())

    def get_connection_helper(self):
        return self._connection_helper

    def finish(self) -> None:
        """
        Close the connection to the database and the SSH tunnel.

        :return: None
        """
        self._connection_helper.close_connection()
