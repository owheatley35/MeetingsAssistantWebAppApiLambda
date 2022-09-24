from enum import Enum


class RolePermission(Enum):
    """
    Permission Types for an action a user can perform.
    """
    # General
    GET_USER_ROLE = "retrieve:role"

    # Meeting Permissions
    MEETING_CREATE = "create:meeting"
    MEETING_UPDATE = "update:meeting"
    MEETING_DELETE = "delete:meeting"
    MEETING_RETRIEVE = "retrieve:meeting"

    # Note Permissions
    NOTE_CREATE = "create:note"
    NOTE_UPDATE = "update:note"
    NOTE_DELETE = "delete:note"
    NOTE_RETRIEVE = "retrieve:note"
