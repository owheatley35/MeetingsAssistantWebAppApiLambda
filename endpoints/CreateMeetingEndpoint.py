from datetime import datetime

from data.creator.MeetingCreator import MeetingCreator
from helper.LoggingHelper import LoggingHelper
from helper.StringHelper import convert_str_to_datetime, convert_comma_seperated_string_to_list


class CreateMeetingEndpoint:
    """
    Endpoint to create a new meeting.

    This should only be used as a secure endpoint since private data can be accessed.
    Ensure that the user ID is validated through Auth0 before sending it into the class.
    """

    def __init__(self, user_id: str, meeting_title: str, meeting_transcript: str, meeting_date: str, meeting_time: str, attendees: str, logger=LoggingHelper(__name__).retrieve_logger()):
        """
        Converts data into correct datatypes and sets up the meeting to be added to the database.

        :param user_id: string of the user id provided by Auth0
        :param meeting_title: string with the title of the meeting
        :param meeting_transcript: string with a description of the meeting
        :param meeting_date: string with the date of the meeting in the format of YYYY-MM-DD
        :param meeting_time: string with the time of the meeting in the format of HH:MM
        :param attendees: comma seperated list of the attendees
        """

        self._logger = logger
        self._user_id: str = user_id
        self._meeting_title: str = meeting_title
        self._meeting_date_time: datetime = convert_str_to_datetime(meeting_date, meeting_time)
        self._attendees = convert_comma_seperated_string_to_list(attendees)
        self._meeting_transcript = meeting_transcript
        self._endpoint_status: bool = True
        self._meeting_creator = MeetingCreator(self._user_id, self._meeting_title, self._meeting_transcript, self._meeting_date_time, self._attendees)

    def create_meeting(self) -> [bool, bool]:
        """
        Calls the creator class to create the meeting when the endpoint is open.

        :return: boolean whether it was successful
        """
        if self._endpoint_status:
            self._logger.info("Creating Endpoint")
            is_success, params_valid = self._meeting_creator.send_meeting()
            self._endpoint_status = False
            return is_success, params_valid
        else:
            self._logger.warning("Meeting not created since Endpoint Closed")
            return False, True

    def close_endpoint(self) -> None:
        """
        Close the endpoint

        :return: None
        """
        self._meeting_creator.finish()
        self._endpoint_status = False
        self._logger.info("Endpoint Closed")
