from datetime import datetime

from data.MeetingDataManipulator import MeetingDataManipulator
from database.MySQLQueryExecutor import MySQLQueryExecutor
from helper.LoggingHelper import LoggingHelper
from helper.SQLValidationHelper import validate_user_id, validate_meeting_id, \
    validate_sql_text, validate_sql_longtext

SQL_QUERY = """UPDATE meetingsassistant.meetings
SET MeetingTitle = %(meeting_title)s, MeetingDateTime = %(meeting_date_time)s, MeetingTranscript = %(meeting_transcript)s 
WHERE UserId = %(user_id)s AND MeetingId = %(meeting_id)s;"""


class MeetingUpdater(MeetingDataManipulator):
    """
    Update meeting information (Title, description and datetime)
    """

    def __init__(self, user_id: str, meeting_id: int, new_title: str, new_description: str, new_datetime: datetime,
                 logger=LoggingHelper(__name__).retrieve_logger()):
        """
        :param new_title: string containing the new meeting title
        :param new_description: string containing the new meeting description
        :param new_datetime: datetime with the new date and time of the meeting
        """

        super().__init__(user_id, meeting_id)
        self._new_title = new_title
        self._new_description = new_description
        self._new_datetime = new_datetime
        self._logger = logger

    def send_update(self) -> bool:
        """
        Executes the query to update the meeting. Only if the connection is open and the parameters are valid.

        :return: boolean whether update was sent
        """
        if self._connection_helper.is_connection_open() and self._is_params_valid():
            self._logger.info("Connection open and Parameters Valid")

            query_helper = MySQLQueryExecutor(self._connection_helper.get_connection_cursor())
            query_helper.execute_query(SQL_QUERY, {
                'user_id': self._user_id,
                'meeting_id': self._meeting_id,
                'meeting_title': self._new_title,
                'meeting_date_time': self._new_datetime,
                'meeting_transcript': self._new_description
            })

            self._connection_helper.commit_connection()
            self._logger.info("Query Completed")

            return True

        self._logger.error("Meeting was not updated on database due to one of the following being 'flase':"
                           "\n Connection Open: %s \n Parameters Valid: %s",
                           str(self._connection_helper.is_connection_open()), str(self._is_params_valid()))
        return False

    def _is_params_valid(self) -> bool:
        """
        Checks whether the parameters to be added to the database are valid against the requirements for the database
        data schema.

        Meeting note validation happens in endpoint class since it must be checked before the string is concatenated
        Meeting note checks in this method are more basic than the full checks.

        :return: boolean whether the parameters are valid
        """

        return validate_user_id(self._user_id) and validate_meeting_id(self._meeting_id) and \
               validate_sql_longtext(self._new_description) and validate_sql_text(self._new_title)
