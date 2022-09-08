from typing import List

from data.provider.meeting.MeetingProvider import MeetingProvider
from data.updater.NoteUpdater import NoteUpdater
from helper.LoggingHelper import LoggingHelper
from helper.StringHelper import break_string_into_list, convert_list_into_string


class DeleteNoteEndpoint:
    """
    Endpoint to delete a specific note from our database using the user id, meeting id and note index
    """

    def __init__(self, user_id: str, meeting_id: str, meeting_note_index: int, logger=LoggingHelper(__name__).retrieve_logger()):
        """
        Retrieves and Converts data to the needed types for addition to the database, including validation.

        :param user_id: string id of the user provided by Auth0
        :param meeting_id: string containing the meeting id as a number in the string
        :param meeting_note_index: int containing the index of the note to delete
        """
        self._logger = logger
        self._user_id: str = user_id
        self._meeting_id: int = int(meeting_id)
        self._endpoint_status: bool = True

        meeting_notes: str = MeetingProvider(self._user_id, self._meeting_id).retrieve_meetings().meeting_notes
        self._meeting_notes: List[str] = break_string_into_list(meeting_notes)

        # Only delete a note if the index exists
        if 0 <= meeting_note_index < len(self._meeting_notes):
            del self._meeting_notes[meeting_note_index]
            self._logger.info("Note Found Successfully")
        else:
            self._logger.error("Invalid index")
            self.close_endpoint()

    def delete_note(self) -> None:
        """
        Complete the deletion of the note.

        :return: None
        """
        if self._endpoint_status:
            self._logger.info("Deleting Note in Progress")
            new_note: str = convert_list_into_string(self._meeting_notes)
            note_updater = NoteUpdater(self._user_id, self._meeting_id, new_note)
            note_updater.send_note()
            note_updater.finish()
        else:
            self._logger.warning("Endpoint Closed")

    def close_endpoint(self) -> None:
        """
        Close the endpoint.

        :return: None
        """
        self._endpoint_status = False
        self._logger.info("Endpoint Closed")
