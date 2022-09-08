import datetime
import logging

from data.MeetingDataManipulator import MeetingDataManipulator
from data.model.meeting.Meeting import Meeting
from database.MySQLQueryExecutor import MySQLQueryExecutor
from helper.LoggingHelper import LoggingHelper
from helper.SQLValidationHelper import validate_meeting_id, validate_user_id

SQL_QUERY = """SELECT MeetingId, MeetingTitle, NumberOfAttendees, MeetingDateTime, MeetingTranscript, MeetingNotes 
FROM MeetingsAssistantInitial.meetings WHERE UserId = %(user_id)s AND MeetingId = %(meeting_id)s"""


class MeetingProvider(MeetingDataManipulator):
    """
    Provider to get a meeting from its ID, only if the meeting belongs to the user.
    """

    def __init__(self, user_id: str, meeting_id: int, logger=LoggingHelper(__name__).retrieve_logger()):
        """
        Formats the required data and opens a database connection.
        Retrieves the meeting information only if all the parameters are valid.

        :param user_id: string id of the user provided by Auth0
        :param meeting_id: int for the meeting id
        """

        super().__init__(user_id, meeting_id)
        self._logger = logger
        self._result: Meeting = Meeting(0, "", datetime.datetime.now(), 0, "", "")

        if self._is_params_valid():
            self._logger.info("Valid Params")
            self._result = self._get_meeting_information()
        else:
            self._logger.error("Invalid Params")

    def retrieve_meetings(self) -> Meeting:
        """
        :return: Meeting that was retrieved from the database.
        """
        return self._result

    def _is_params_valid(self) -> bool:
        """
        Checks whether the parameters for the query are valid.

        :return: boolean describing whether the parameters are valid
        """
        return validate_user_id(self._user_id) and validate_meeting_id(self._meeting_id)

    def _get_meeting_information(self) -> Meeting:
        """
        Executes the query to gather the meeting data and format as a Meeting object.
        Only run if the connection is open

        :return: Meeting object containing the meeting data
        """

        if self._connection_helper.is_connection_open():
            self._logger.info("Connection Open")

            query_helper = MySQLQueryExecutor(self._connection_helper.get_connection_cursor())
            rows_returned = query_helper.execute_query(SQL_QUERY, {
                'user_id': self._user_id,
                'meeting_id': self._meeting_id
            })

            for row in rows_returned:
                temp_meeting = Meeting(row[0], row[1], row[3], row[2], row[4], row[5])
                self._logger.info("Query Successful")
                return temp_meeting

            self._logger.warning("No Meeting Found")

        self._logger.error("Connection is not open")
