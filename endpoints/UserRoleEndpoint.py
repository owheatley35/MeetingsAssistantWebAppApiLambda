from data.model.Response import Response
from data.provider.UserRoleProvider import UserRoleProvider
from helper.LoggingHelper import LoggingHelper


class UserRoleEndpoint:

    def __init__(self, user_id: str, logger=LoggingHelper(__name__).retrieve_logger()):
        self._logger = logger
        self._logger.info("UserRoleEndpoint: Starting Endpoint")

        self._user_id = user_id
        self._role_provider = UserRoleProvider(self._user_id)
        self._endpoint_status = True

    def get_user_role(self) -> Response:
        if self._endpoint_status:
            return Response(True, self._role_provider.get_user_role())
        else:
            self._logger.info("Endpoint: UserRoleEndpoint - Closed")
            Response(False)

    def close_endpoint(self) -> None:
        """
        Close the endpoint

        :return: None
        """
        self._role_provider.finish()
        self._endpoint_status = False
        self._logger.info("UserRoleEndpoint: Endpoint Closed")
