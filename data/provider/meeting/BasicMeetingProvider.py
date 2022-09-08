from typing import List

from data.DatabaseConnector import DatabaseConnector
from data.model.meeting.BasicMeeting import BasicMeeting
from database.MySQLQueryExecutor import MySQLQueryExecutor
from helper.LoggingHelper import LoggingHelper
from helper.SQLValidationHelper import validate_user_id

BASIC_MEETING_QUERY = """SELECT MeetingId, MeetingTitle, NumberOfAttendees, MeetingDateTime FROM MeetingsAssistantInitial.meetings WHERE UserId = %(user_id)s"""

# datetime format
f = '%Y-%m-%d %H:%M:%S'


class BasicMeetingProvider(DatabaseConnector):
    """
    Retrieves all meetings for an Auth0 user id in a Basic formatting.
    """

    def __init__(self, user_id: str, logger=LoggingHelper(__name__).retrieve_logger()):
        """
        Open a database connection and retrieve the basic meetings.

        :param user_id: string id of the user provided by Auth0
        """
        super().__init__()

        self._logger = logger
        self._result: List[BasicMeeting] = []
        self._user_id: str = user_id

        if validate_user_id(self._user_id):
            self._logger.info("User ID valid")
            self._result = self._get_meeting_information()

    def refresh_data(self) -> None:
        """
        Re-run the query to get new data.

        :return: None
        """
        self._logger.info("Refreshing Data")
        self._result = self._get_meeting_information()

    def get_meeting_info(self) -> List[BasicMeeting]:
        """
        Retrieves the list of basic meetings from the query.

        :return: A List of BasicMeetings
        """
        return self._result

    def _get_meeting_information(self) -> List[BasicMeeting]:
        """
        Executes the query to gather all the basic meetings from the database.
        Only runs if the user id is valid and the connection is open.

        :return: List of Basic Meetings (empty if none found or connection closed)
        """
        result = []

        if validate_user_id(self._user_id) and self._connection_helper.is_connection_open():
            self._logger.info("Params valid and Connection open")

            query_helper = MySQLQueryExecutor(self._connection_helper.get_connection_cursor())
            rows_returned = query_helper.execute_query(BASIC_MEETING_QUERY, {
                'user_id': self._user_id
            })

            for row in rows_returned:
                temp_meeting = BasicMeeting(row[0], row[1], row[3], row[2])
                result.append(temp_meeting)
        else:
            self._logger.error("Query was not sent to database due to one of the following being "
                               "'flase': \n Connection Open: %s \n Parameters Valid: %s",
                               str(self._connection_helper.is_connection_open()), str(validate_user_id(self._user_id)))

        if len(result) > 0:
            self._logger.info("Query Successful")
        else:
            self._logger.error("No data found from query.")

        return result
