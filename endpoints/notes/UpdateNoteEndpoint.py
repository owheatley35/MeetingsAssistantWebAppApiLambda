import logging
from typing import List

from data.provider.meeting.MeetingProvider import MeetingProvider
from data.updater.NoteUpdater import NoteUpdater
from helper.LoggingHelper import LoggingHelper
from helper.SQLValidationHelper import validate_meeting_note
from helper.StringHelper import break_string_into_list, convert_list_into_string


class UpdateNoteEndpoint:
    """
    Endpoint to Update a specific note in the database.

    This should only be used as a secure endpoint since private data can be accessed.
    Ensure that the user ID is validated through Auth0 before sending it into the class.
    """

    def __init__(self, user_id: str, meeting_id: str, meeting_note_content: str, meeting_note_index: int,
                 logger=LoggingHelper(__name__).retrieve_logger()):
        """
        Updates the meeting note string to include the new note provided. It does this by converting the existing string
        into a List and then updates the intended index with the new value.

        :param user_id: string id of the user provided by Auth0
        :param meeting_id: string containing the meeting id as a number in the string
        :param meeting_note_content: String of the new meeting note
        :param meeting_note_index: int of the index of the note to update
        """
        self._logger = logger
        self._user_id: str = user_id
        self._meeting_id: int = int(meeting_id)
        self._endpoint_status: bool = True

        meeting_notes: str = MeetingProvider(self._user_id, self._meeting_id).retrieve_meetings().meeting_notes
        self._meeting_notes: List[str] = break_string_into_list(meeting_notes)

        if validate_meeting_note(meeting_note_content):
            self._logger.info("Meeting Note Valid")
            self._meeting_notes[meeting_note_index] = meeting_note_content
        else:
            self._logger.error("Invalid note")
            self.close_endpoint()

    def update_note(self) -> None:
        """
        Calls the note updater to update the note value at the configured index.
        Only runs if the endpoint is active.

        :return: None
        """

        if self._endpoint_status:
            self._logger.info("Starting update of note")
            new_note: str = convert_list_into_string(self._meeting_notes)
            note_updater = NoteUpdater(self._user_id, self._meeting_id, new_note)
            note_updater.send_note()
            note_updater.finish()
        else:
            self._logger.warning("Unable to update note: Endpoint closed")

    def close_endpoint(self) -> None:
        """
        Closes the Endpoint.
        :return: None
        """
        self._endpoint_status = False
        self._logger.info("Endpoint Closed")
