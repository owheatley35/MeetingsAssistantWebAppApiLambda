from unittest import TestCase

from security.roles.RolePermission import RolePermission
from security.roles.User import User

USER_ID = "jvnej13j3fi"
VALID_ROLE = "role:standard"
VALID_STANDARD_PERMISSION = RolePermission.MEETING_RETRIEVE
INVALID_STANDARD_PERMISSION = RolePermission.MEETING_DELETE
INVALID_ROLE = "not:a:role"


class UserTest(TestCase):

    def test_user_creation_successful(self):
        testee_user = User(USER_ID, VALID_ROLE)
        self.assertEqual(testee_user.get_id(), USER_ID)

    def test_user_creation_failed(self):
        self.assertRaises(Exception, User, USER_ID, INVALID_ROLE)

    def test_is_authorised(self):
        testee = User(USER_ID, VALID_ROLE)
        self.assertTrue(testee.is_authorised({VALID_STANDARD_PERMISSION}))

    def test_is_not_authorised(self):
        testee = User(USER_ID, VALID_ROLE)
        self.assertFalse(testee.is_authorised({INVALID_STANDARD_PERMISSION}))
