class DBConfiguration:
    """
    Class to model all data needed to establish a connection to the MySQL Database.
    """

    def __init__(self, db_host: str, db_username: str, db_password: str,
                 db_port: str, db_name: str):
        """
        :param db_host: string containing the host for the database
        :param db_username: username for the database
        :param db_password: password for the database
        :param db_port: port number for the database connection
        :param db_name: db name
        """

        self._host = db_host
        self._db_username = db_username
        self._db_password = db_password
        self._port = db_port
        self._db_name = db_name
        self._db_connection_timeout = 5

    def get_db_host(self) -> str:
        return self._host

    def get_db_username(self) -> str:
        return self._db_username

    def get_db_password(self) -> str:
        return self._db_password

    def get_port(self) -> str:
        return self._port

    def get_db_name(self) -> str:
        return self._db_name

    def get_db_connection_timeout(self) -> int:
        return self._db_connection_timeout
