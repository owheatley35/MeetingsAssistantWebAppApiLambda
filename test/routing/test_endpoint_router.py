from unittest import TestCase
from unittest.mock import Mock

from mockito import mock, when

from routing.EndpointExecutor import EndpointExecutor
from response.SetResponses import SetResponses
from security.roles.User import User
from routing.endpoint_router import EndpointRouter

USER = User("userid", "role:standard")
VALID_PATH = "/get/all-basic-meetings"
VALID_ADMIN = "/delete/meeting-note"
VALID_RESPONSE = "VALID"
executor = Mock()
executor_mock = mock(EndpointExecutor)


class EndpointRouterTest(TestCase):

    def test_invalid_route(self):
        path: str = "/get.not-real"

        testee = EndpointRouter(executor, path)
        result = testee.route_endpoint()

        self.assertEqual(result, SetResponses.INVALID_ROUTE.value)

    def test_unauthorised_user(self):
        when(executor_mock).get_user().thenReturn(USER)
        testee = EndpointRouter(executor_mock, VALID_ADMIN)
        result = testee.route_endpoint()

        self.assertEqual(result, SetResponses.UNAUTHORIZED.value)

    def test_correct_route(self):
        when(executor_mock).get_user().thenReturn(USER)
        when(executor_mock).execute_get_all_meetings().thenReturn(VALID_RESPONSE)
        testee = EndpointRouter(executor_mock, VALID_PATH)
        result = testee.route_endpoint()

        self.assertEqual(VALID_RESPONSE, result)
