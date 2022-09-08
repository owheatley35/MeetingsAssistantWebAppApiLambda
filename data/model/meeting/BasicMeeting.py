from datetime import datetime


class BasicMeeting:
    """
    Class to model a basic meeting, used for display of meetings on the home page.
    """

    def __init__(self, meeting_id: int, meeting_title: str, meeting_date_time: datetime, number_of_attendees: int):
        self.meeting_title = meeting_title
        self.meeting_id = meeting_id
        self.number_of_attendees = number_of_attendees
        self.meeting_date = str(meeting_date_time.date())
        self.meeting_time = str(meeting_date_time.time())
