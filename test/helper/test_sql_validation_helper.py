from unittest import TestCase

from helper.SQLValidationHelper import validate_user_id


class TestSQLValidationHelper(TestCase):

    def test_validate_user_id(self):
        test_data = "ddv48g5gggd588djhd84d8d8d8ddd63"
        result = validate_user_id(test_data)

        self.assertTrue(result)

    def test_validate_user_id_too_long(self):
        test_data = "djdjdjdjdjdkjkdjkjbjhfujhfuirwhf87878frnrjfbjrfbjrbfjbfjrbjfbrjfbjrbfjrbfjrbfjrbjfbrjfbrjbfjrbjbwvbrjkbvhjerbvjbjbjbvjerbjbfjrbfjrbfjrbfrjfrf8f85f8f5f8f5f8f5f8f5f85f8f5f8f5fd8vrff5r4e87fr94f5r4f8re48fr5f48er64f8r486r4f84r684fr84f8r4f86r48f4r8f48r64f8r4f864re84f8r4f8r4fe64fer864f6re4f8r468ef4r86e4f86re4f8r6e4f8re4f8r4f8r484fe68f46er84fr86e4fer84fr64frfjkbujerbfebiubvj"
        result = validate_user_id(test_data)

        self.assertFalse(result)

    def test_validate_user_id_invalid_pattern(self):
        test_data = "rhfr & 52"
        result = validate_user_id(test_data)

        self.assertFalse(result)

    def test_validate_user_id_cap(self):
        test_data = "jdbnvhwvHHHJowsiueb"
        result = validate_user_id(test_data)

        self.assertFalse(result)
