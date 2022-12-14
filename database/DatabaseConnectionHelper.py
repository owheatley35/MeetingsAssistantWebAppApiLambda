from helper.LoggingHelper import LoggingHelper
from mysql.connector import connect


class DatabaseConnectionHelper:
    """
    Class to create and manage the SSH Tunnel and MySLQ DB connection.
    """

    def __init__(self, configuration, logger=LoggingHelper(__name__).retrieve_logger()):
        """
        Establishes a DB Connection to RDS

        :param configuration: DBConfiguration Details
        """
        self._logger = logger
        self._is_connected = False
        self._configuration = configuration
        self._connection = self._establish_connection()
        self._logger.info("MySQL DB Connection Established")

    def get_connection_cursor(self):
        """
        Retrieve the connection cursor

        :return: The connection cursor from the connection helper
        """
        return self._connection.cursor()

    def commit_connection(self) -> None:
        """
        Run the commit command on the ssh connection.
        Required when running insert or update SQL commands.

        :return: None
        """
        self._connection.commit()

    def close_connection(self) -> None:
        """
        Close the connection to the database if the connection is open.

        :return: None
        """

        if self._is_connected:
            self._connection.close()
            self._logger.info("DB Connection Closed Successfully")

    def is_connection_open(self) -> bool:
        """
        Checks if a connection to the database exists and if a tunnel is active to the EC2 instance

        :return: boolean whether a connection is active
        """
        return self._is_connected

    def _establish_connection(self):
        """
        Opens the SSH tunnel and uses it to establish a connection to the SQl database

        :return: Connection to MySQL database
        """
        self._logger.info("Opening Connection")

        try:
            # conn = pymysql.connect(
            #     host=self._configuration.get_db_host(),
            #     user=self._configuration.get_db_username(),
            #     passwd=self._configuration.get_db_password(),
            #     port=self._configuration.get_port(),
            #     connect_timeout=self._configuration.get_db_connection_timeout()
            # )
            conn = connect(
                user=self._configuration.get_db_username(),
                password=self._configuration.get_db_password(),
                host=self._configuration.get_db_host(),
                port=self._configuration.get_port(),
            )
            self._is_connected = True
            self._logger.info("Connection Opened")
            return conn
        except Exception as e:
            self._is_connected = False
            self._logger.error("Connection Failed" + str(e))
            return

