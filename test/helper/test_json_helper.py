from typing import List
from unittest import TestCase

from helper.JSONHelper import convert_custom_object_list_to_dict
from security.roles.User import User


class TestJSONHelper(TestCase):

    def test_convert_custom_object_list_to_dict(self):
        test_data: List[object] = [User('01', 'role:standard'), User('02', 'role:admin')]
        result = convert_custom_object_list_to_dict(test_data)

        self.assertEqual(result[0].get('_user_id'), '01')
        self.assertEqual(result[1].get('_user_id'), '02')
