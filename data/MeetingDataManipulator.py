from data.DatabaseConnector import DatabaseConnector


class MeetingDataManipulator(DatabaseConnector):
    """
    Super class of classes that need to interact with any element in the meeting table of the database.
    """

    def __init__(self, user_id: str, meeting_id: int):
        super().__init__()
        self._user_id = user_id
        self._meeting_id = meeting_id
