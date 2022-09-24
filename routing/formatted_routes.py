from enum import Enum


class FormattedRoutes(Enum):
    GetAllMeetings = "get-all-basic-meetings"
    GetMeetingFromId = "get-meeting-from-id"
    UpdateMeetingNote = "update-meeting-note"
    CreateMeetingNote = "create-meeting-note"
    DeleteMeetingNote = "delete-meeting-note"
    CreateMeeting = "create-meeting"
    DeleteMeeting = "delete-meeting"
    GetUserRole = "get-user-role"
    UpdateMeetingDetails = "update-meeting-details"
