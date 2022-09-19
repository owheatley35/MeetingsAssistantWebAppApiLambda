from unittest import TestCase

from routing.EndpointExecutor import EndpointExecutor
from security.roles.User import User

TEST_ARGS = {
    "arg1": "value1"
}

USER = User("id-test", "role:standard")


class TestEndpointExecutor(TestCase):

    def test_get_user(self):
        executor = EndpointExecutor(USER, TEST_ARGS)
        result = executor.get_user()

        self.assertEqual(result.get_id(), USER.get_id())
