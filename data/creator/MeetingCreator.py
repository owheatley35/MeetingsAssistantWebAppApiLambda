import logging
from datetime import datetime
from typing import List

from data.DatabaseConnector import DatabaseConnector
from database.MySQLQueryExecutor import MySQLQueryExecutor
from helper.LoggingHelper import LoggingHelper
from helper.SQLValidationHelper import validate_user_id, validate_sql_text, validate_sql_longtext
from helper.StringHelper import convert_list_to_comma_seperated_string

SQL_QUERY = """insert into MeetingsAssistantInitial.meetings (UserId, MeetingDateTime, NumberOfAttendees, MeetingTranscript, MeetingTitle, attendees)
values (%(user_id)s, %(meeting_date_time)s, %(number_of_attendees)s, %(meeting_description)s, %(meeting_title)s, %(attendees)s);"""


class MeetingCreator(DatabaseConnector):
    """
    Class to create a Meeting.
    """

    def __init__(self, user_id: str, meeting_title: str, meeting_description: str, meeting_date_time: datetime,
                 attendees: List[str], logger=LoggingHelper(__name__).retrieve_logger()):
        """
        Sets up dependencies and data required to  create a new meeting, including opening a DB connection

        :param user_id: string id of the user provided by Auth0
        :param meeting_title: string describing the meeting title
        :param meeting_description: string describing the meeting description
        :param meeting_date_time: datetime object for the date and time of the meeting taking place
        :param attendees: List of string containing names or alias' of those who attended the meeting
        """

        super().__init__()
        self._logger = logger
        self._user_id = user_id
        self._meeting_title = meeting_title
        self._meeting_description = meeting_description
        self._meeting_date_time = meeting_date_time
        self._attendees = convert_list_to_comma_seperated_string(attendees)
        self._number_of_attendees = len(attendees)

    def send_meeting(self) -> None:
        """
        Creates a new meeting in the database.
        Only runs if a connection is open and the parameters are valid

        :return: None
        """
        if self._connection_helper.is_connection_open() and self._is_params_valid():

            self._logger.info("Connection open and Params Valid")

            query_helper = MySQLQueryExecutor(self._connection_helper.get_connection_cursor())
            query_helper.execute_query(SQL_QUERY, {
                'user_id': self._user_id,
                'meeting_title': self._meeting_title,
                'meeting_description': self._meeting_description,
                'meeting_date_time': self._meeting_date_time,
                'attendees': self._attendees,
                'number_of_attendees': self._number_of_attendees
            })

            self._connection_helper.commit_connection()
        else:
            self._logger.error("Meeting was not created in database due to one of the following being "
                               "'flase': \n Connection Open: %s \n Parameters Valid: %s",
                               str(self._connection_helper.is_connection_open()), str(self._is_params_valid()))

    def _is_params_valid(self) -> bool:
        """
        Checks whether the parameters to be added to the database are valid against the database data schema.

        :return: boolean describing if the parameters are valid
        """
        return validate_user_id(self._user_id) and validate_sql_text(self._meeting_title) and \
               validate_sql_longtext(self._meeting_description) and validate_sql_longtext(self._attendees)
