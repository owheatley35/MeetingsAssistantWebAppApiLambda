from data.DatabaseConnector import DatabaseConnector
from database.MySQLQueryExecutor import MySQLQueryExecutor
from helper.LoggingHelper import LoggingHelper
from helper.SQLValidationHelper import validate_user_id

SQL_QUERY = "SELECT RoleName FROM meetingsassistant.users WHERE UserId = %(user_id)s"


class UserRoleProvider(DatabaseConnector):
    """
    Provides the role that the user is assigned.
    """

    def __init__(self, user_id: str, logger=LoggingHelper(__name__).retrieve_logger()):
        """
        :param user_id: Unique identification of the user provided by Auth0
        """
        super().__init__()
        self._logger = logger
        self._user_id = user_id
        self._result = ""

        if self._is_params_valid():
            self._logger.info("Parameters Valid")
            self._result = self._get_role()
        else:
            self._logger.error("Invalid Parameters")

    def get_user_role(self) -> str:
        """
        Retrieves the user role or empty string if nothing was found.

        :return: string of the user role
        """
        return self._result if self._result else ""

    def _is_params_valid(self) -> bool:
        """
        Checks if parameters are valid.

        :return: boolean whether parameters are valid
        """
        return validate_user_id(self._user_id)

    def _get_role(self):
        """
        Calls the query to get the user role from the database.

        :return: Users role string
        """

        if self._connection_helper.is_connection_open() and self._is_params_valid():

            self._logger.info("Connection Open and Params Valid")

            query_helper = MySQLQueryExecutor(self._connection_helper.get_connection_cursor())
            rows_returned = query_helper.execute_query(SQL_QUERY, {
                'user_id': self._user_id,
            })

            for row in rows_returned:
                self._logger.info("Query Completed Successfully")
                return rows_returned[0][0]

            self._logger.warning("Query Returned NO Results")

        self._logger.error("Database not Queried due to one of the following being 'flase': \n "
                           "Connection Open: %s \n Parameters Valid: %s",
                           str(self._connection_helper.is_connection_open()), str(self._is_params_valid()))
