from datetime import datetime

from data.model.meeting.BasicMeeting import BasicMeeting


class Meeting(BasicMeeting):
    """
    Class to model a Meeting
    """

    def __init__(self, meeting_id: int, meeting_title: str, meeting_date_time: datetime, number_of_attendees: int,
                 meeting_transcript: str, meeting_notes: str):
        super().__init__(meeting_id, meeting_title, meeting_date_time, number_of_attendees)
        self.meeting_transcript = meeting_transcript
        self.meeting_notes = meeting_notes
