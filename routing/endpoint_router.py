import re

from routing.EndpointExecutor import EndpointExecutor
from helper.LoggingHelper import LoggingHelper
from response.SetResponses import SetResponses
from security.roles.RoleConfiguration import route_security_configuration
from routing.formatted_routes import FormattedRoutes


class EndpointRouter:
    """
    Routes request to the correct endpoint.
    """

    def __init__(self, endpoint_executor: EndpointExecutor, path: str,
                 logger=LoggingHelper(__name__).retrieve_logger()):
        """
        Open an instance of the EndpointRouter class and set the user id, path, and query parameters.

        :param endpoint_executor: Interface with endpoint execution for the user
        :param path: string of the path provided by the request
        """
        self._path = path
        self._user = endpoint_executor.get_user()
        self._logger = logger
        self._endpoint_executor = endpoint_executor

    def route_endpoint(self):
        """
        Route the request to the correct endpoint.

        :return: Response from the endpoint formatted to be sent to the client
        """
        formatted_route = self._format_route()
        self._logger.info("Formatted Route: " + formatted_route)

        # Check route is valid
        if formatted_route not in [member.value for member in FormattedRoutes]:
            return self._invalid_response(formatted_route)

        # Check user is authorised - only continue if true
        if not self._user.is_authorised(route_security_configuration.get(formatted_route)):
            self._logger.error("User not authorised to access {} endpoint.".format(FormattedRoutes.GetAllMeetings))
            return SetResponses.UNAUTHORIZED.value

        # Route to correct endpoint - no switch statement in python :(
        if formatted_route == FormattedRoutes.GetAllMeetings.value:
            return self._endpoint_executor.execute_get_all_meetings()
        elif formatted_route == FormattedRoutes.GetMeetingFromId.value:
            return self._endpoint_executor.execute_get_meeting_from_id()
        elif formatted_route == FormattedRoutes.UpdateMeetingNote.value:
            return self._endpoint_executor.execute_update_meeting_note()
        elif formatted_route == FormattedRoutes.CreateMeetingNote.value:
            return self._endpoint_executor.execute_create_meeting_note()
        elif formatted_route == FormattedRoutes.DeleteMeetingNote.value:
            return self._endpoint_executor.execute_delete_meeting_note()
        elif formatted_route == FormattedRoutes.CreateMeeting.value:
            return self._endpoint_executor.execute_create_meeting()
        elif formatted_route == FormattedRoutes.DeleteMeeting.value:
            return self._endpoint_executor.execute_delete_meeting()
        elif formatted_route == FormattedRoutes.GetUserRole.value:
            return self._endpoint_executor.execute_get_user_role()
        elif formatted_route == FormattedRoutes.UpdateMeetingDetails.value:
            return self._endpoint_executor.execute_update_meeting_details()
        else:
            # Covers all routes that are not currently implemented but exist in the enum
            return self._invalid_response(formatted_route)

    def _format_route(self) -> str:
        """
        Format the path to a string that can be used to route the request to the correct endpoint.
        Follows format in lower case: <operation>-<resourceName> eg. get-all-basic-meetings

        :return: string of the formatted route
        """
        string_with_character_removed = self._path[1:]
        return string_with_character_removed.replace("/", "-").lower()

    def _invalid_response(self, route: str):
        """
        Return a response indicating the route is invalid.

        :param route: string of the route
        :return: response indicating the route is invalid
        """
        self._logger.error("Invalid route: " + route)
        return SetResponses.INVALID_ROUTE.value
