import threading

from endpoints.CreateMeetingEndpoint import CreateMeetingEndpoint
from endpoints.DeleteMeetingEndpoint import DeleteMeetingEndpoint
from endpoints.EditMeetingEndpoint import EditMeetingEndpoint
from endpoints.GetBasicMeetingsEndpoint import GetBasicMeetingsEndpoint
from endpoints.GetMeetingEndpoint import GetMeetingEndpoint
from endpoints.UserRoleEndpoint import UserRoleEndpoint
from endpoints.notes.CreateNoteEndpoint import CreateNoteEndpoint
from endpoints.notes.DeleteNoteEndpoint import DeleteNoteEndpoint
from endpoints.notes.UpdateNoteEndpoint import UpdateNoteEndpoint
from helper.LoggingHelper import LoggingHelper
from response.ResponseCreator import ResponseCreator
from response.SetResponses import SetResponses
from security.roles.User import User


class EndpointExecutor:
    """
    Provides execution for endpoints and configures their variables.
    """
    def __init__(self, user: User, args: dict, logger=LoggingHelper(__name__).retrieve_logger()):
        """
        Open an instance of the EndpointExecutor class and set the user id and args.

        :param user: User object containing information about the user
        :param args: dictionary of arguments provided by the request
        """
        logger.info(args)
        self._args = args
        self._logger = logger
        self._user: User = user

    def execute_get_all_meetings(self):
        """
        Executes the GetBasicMeetingsEndpoint and returns the result.
        """
        self._logger.info("Executing: 'Get All Meetings'")
        endpoint = GetBasicMeetingsEndpoint(self._user.get_id())
        endpoint_result = endpoint.get_endpoint_result()
        threading.Thread(target=endpoint.close_endpoint).start()
        return self._generate_response(endpoint_result, True)

    def execute_get_meeting_from_id(self):
        """
        Executes the GetMeetingEndpoint and returns the result.
        """
        self._logger.info("Executing: 'Get Meeting From ID'")
        meeting_id = self._args["meeting_id"]
        endpoint = GetMeetingEndpoint(self._user.get_id(), meeting_id)
        endpoint_result = endpoint.get_endpoint_result()
        threading.Thread(target=endpoint.close_endpoint).start()
        return self._generate_response(endpoint_result, True)

    def execute_update_meeting_note(self):
        """
        Executes the UpdateNoteEndpoint and returns the result.
        """
        self._logger.info("Executing: 'Update Meeting Note'")
        meeting_id = self._args["meeting_id"]
        note_content = self._args["note_content"]
        note_index = self._args["note_index"]
        endpoint = UpdateNoteEndpoint(self._user.get_id(), meeting_id, note_content, note_index)
        endpoint.update_note()
        endpoint.close_endpoint()
        return self._generate_set_response(True)

    def execute_create_meeting_note(self):
        """
        Executes the CreateNoteEndpoint and returns the result.
        """
        self._logger.info("Executing: 'Create Meeting Note'")
        meeting_id = self._args["meeting_id"]
        note_content = self._args["note_content"]
        endpoint = CreateNoteEndpoint(self._user.get_id(), meeting_id, note_content)
        is_success = endpoint.create_note()
        endpoint.close_endpoint()
        return self._generate_set_response(is_success)

    def execute_delete_meeting_note(self):
        """
        Executes the DeleteNoteEndpoint and returns the result.
        """
        self._logger.info("Executing: 'Delete Meeting Note'")
        meeting_id = self._args["meeting_id"]
        note_index = self._args["note_index"]
        endpoint = DeleteNoteEndpoint(self._user.get_id(), meeting_id, note_index)
        is_success = endpoint.delete_note()
        endpoint.close_endpoint()
        return self._generate_set_response(is_success)

    def execute_create_meeting(self):
        """
        Executes the CreateMeetingEndpoint and returns the result.
        """
        self._logger.info("Executing: 'Create Meeting'")
        meeting_name = self._args["meeting_title"]
        meeting_description = self._args["meeting_description"]
        meeting_date = self._args["meeting_date"]
        meeting_time = self._args["meeting_time"]
        meeting_attendees = self._args["meeting_attendees"]
        endpoint = CreateMeetingEndpoint(self._user.get_id(), meeting_name, meeting_description, meeting_date, meeting_time, meeting_attendees)
        is_success, params = endpoint.create_meeting()
        endpoint.close_endpoint()
        return self._generate_set_response(is_success) if params else SetResponses.INVALID_REQUEST

    def execute_delete_meeting(self):
        """
        Executes the DeleteMeetingEndpoint and returns the result.
        """
        self._logger.info("Executing: 'Delete Meeting'")
        meeting_id = self._args["meeting_id"]
        endpoint = DeleteMeetingEndpoint(self._user.get_id(), meeting_id)
        response = endpoint.delete_meeting()
        endpoint.close_endpoint()
        return ResponseCreator(response.get_formatted_response()).generate_successful_response()

    def execute_get_user_role(self):
        """
        Executes the GetUserRoleEndpoint and returns the result.
        """
        self._logger.info("Executing: 'Get User Role'")
        endpoint = UserRoleEndpoint(self._user.get_id())
        endpoint_result = endpoint.get_user_role()
        endpoint.close_endpoint()
        return ResponseCreator(endpoint_result.get_formatted_response()).generate_successful_response()

    def execute_update_meeting_details(self):
        """
        Executes the UpdateMeetingDetailsEndpoint and returns the result.
        """
        self._logger.info("Executing: 'Update Meeting Details'")
        meeting_id = self._args["meeting_id"]
        meeting_name = self._args["meeting_title"]
        meeting_description = self._args["meeting_description"]
        meeting_date = self._args["meeting_date"]
        endpoint = EditMeetingEndpoint(self._user.get_id(), meeting_id, meeting_name, meeting_description, meeting_date)
        result = endpoint.update_meeting()
        endpoint.close_endpoint()
        return ResponseCreator(result.get_formatted_response()).generate_successful_response()

    def get_user(self) -> User:
        return self._user

    def _generate_response(self, body, success: bool):
        if success:
            return ResponseCreator(body).generate_successful_response()
        else:
            return ResponseCreator(body).generate_failure_response()

    def _generate_set_response(self, is_success: bool):
        return SetResponses.BLANK_SUCCESS.value if is_success else SetResponses.INTERNAL_ERROR.value
