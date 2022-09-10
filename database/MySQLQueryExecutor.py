from helper.LoggingHelper import LoggingHelper


class MySQLQueryExecutor:
    """
    Class to manage execution of queries on DB.
    """

    def __init__(self, cursor, logger=LoggingHelper(__name__).retrieve_logger()):
        """
        :param cursor: A cursor object, should be created from the DatabaseConnectionHelper
        """
        self._cursor = cursor
        self._logger = logger

    def execute_query(self, query: str, parameters={}):
        """
        Run a SQL query on a database using the cursor provided.
        Resets the cursor when done.
        
        :param query: String containing the SQL query
        :param parameters: optional - dictionary containing the parameters
        :return: list of rows retrieved from the result of the database
        """
        self._logger.info("Executing Query: " + query.format(parameters))

        rows = []

        try:
            if parameters:
                self._cursor.execute(query, parameters)
            else:
                self._cursor.execute(query)

            self._logger.info("MySQLQueryExecutor: Query Successfully Executed")

        except Exception as e:
            self._logger.error(e)

        for row in self._cursor:
            rows.append(row)

        self._cursor.reset()
        return rows
