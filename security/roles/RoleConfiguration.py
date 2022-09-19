from routing.formatted_routes import FormattedRoutes
from security.roles.RolePermission import RolePermission
from security.roles.RoleType import RoleType

# Define the permissions of each role type.
role_configuration = {
    RoleType.ADMIN: {
        RolePermission.NOTE_CREATE.value,
        RolePermission.NOTE_DELETE.value,
        RolePermission.NOTE_UPDATE.value,
        RolePermission.NOTE_RETRIEVE.value,
        RolePermission.MEETING_CREATE.value,
        RolePermission.MEETING_DELETE.value,
        RolePermission.MEETING_RETRIEVE.value,
        RolePermission.MEETING_UPDATE.value
    },
    RoleType.STANDARD: {
        RolePermission.NOTE_CREATE.value,
        RolePermission.NOTE_UPDATE.value,
        RolePermission.NOTE_RETRIEVE.value,
        RolePermission.MEETING_CREATE.value,
        RolePermission.MEETING_RETRIEVE.value,
        RolePermission.MEETING_UPDATE.value
    }
}

# Define the permissions required for each route.
route_security_configuration = {
    FormattedRoutes.GetAllMeetings.value: {
        RolePermission.MEETING_RETRIEVE
    },
    FormattedRoutes.GetMeetingFromId.value: {
        RolePermission.MEETING_RETRIEVE
    },
    FormattedRoutes.UpdateMeetingNote.value: {
        RolePermission.NOTE_UPDATE
    },
    FormattedRoutes.CreateMeetingNote.value: {
        RolePermission.NOTE_CREATE
    },
    FormattedRoutes.DeleteMeetingNote.value: {
        RolePermission.NOTE_DELETE
    },
    FormattedRoutes.CreateMeeting.value: {
        RolePermission.MEETING_CREATE
    },
    FormattedRoutes.DeleteMeeting.value: {
        RolePermission.MEETING_DELETE
    },
    FormattedRoutes.UpdateMeetingDetails.value: {
        RolePermission.MEETING_UPDATE
    }
}
