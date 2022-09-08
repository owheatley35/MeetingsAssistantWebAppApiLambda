import logging

from data.provider.meeting.MeetingProvider import MeetingProvider
from helper.JSONHelper import convert_custom_object_to_dict
from helper.LoggingHelper import LoggingHelper


class GetMeetingEndpoint:
    """
    Endpoint to retrieve a full Meeting from the database using the Meeting ID and User ID.

    This should only be used as a secure endpoint since private data can be accessed.
    Ensure that the user ID is validated through Auth0 before sending it into the class.
    """

    def __init__(self, user_id: str, meeting_id: str, logger=LoggingHelper(__name__).retrieve_logger()):
        """
        :param user_id: string id of the user (provided by Auth0)
        :param meeting_id: string id of the meeting to be retrieved
        """

        self._logger = logger
        self._logger.info("GetMeetingEndpoint: Starting Endpoint")

        self._user_id: str = user_id
        self._meeting_id: int = int(meeting_id)
        self._endpoint_status: bool = True
        self._meetings_provider: MeetingProvider = MeetingProvider(self._user_id, self._meeting_id)

    def get_endpoint_result(self) -> dict:
        """
        Retrieve the result of this endpoint. This method is only available when the endpoint is open.

        :return: dictionary of the meeting result from the database
        """
        if self._endpoint_status:
            return convert_custom_object_to_dict(self._meetings_provider.retrieve_meetings())

    def close_endpoint(self) -> None:
        """
        Close this endpoint. Should be called in a separate thread, after this endpoint has been finished with.
        :return: None
        """
        self._meetings_provider.finish()
        self._endpoint_status = False
        self._logger.info("GetMeetingEndpoint: Endpoint Closed")
