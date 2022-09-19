import time

from unittest import TestCase
from datetime import datetime

from helper.StringHelper import break_string_into_list, convert_list_into_string, convert_str_to_datetime, \
    convert_list_to_comma_seperated_string, convert_comma_seperated_string_to_list


class TestStringHelper(TestCase):
    def test_break_string_into_list_single_item(self):
        test_data = "hello there."
        result = break_string_into_list(test_data)

        self.assertTrue(test_data in result)

    def test_break_string_into_list(self):
        test_data = "/#&-hello there /#&- new note/#&-finalnote"
        result = break_string_into_list(test_data)

        self.assertEqual(len(result), 3)
        self.assertEqual("hello there", result[0])
        self.assertEqual("new note", result[1])
        self.assertEqual("finalnote", result[2])

    def test_convert_list_into_string(self):
        test_data = ["one", "two", "three"]
        expected_result = "/#&-one/#&-two/#&-three"
        result = convert_list_into_string(test_data)

        self.assertTrue(isinstance(result, str))
        self.assertEqual(result, expected_result)

    def test_convert_str_to_datetime_failure(self):
        first_datetime = datetime.now()
        test_data = "fakedata"
        time.sleep(0.1)
        result = convert_str_to_datetime(test_data, test_data)
        time.sleep(0.1)
        second_datetime = datetime.now()

        self.assertTrue(first_datetime < result)
        self.assertTrue(second_datetime > result)

    def test_convert_str_to_datetime(self):
        date = "2001-04-11"
        time_amount = "12:00"
        result = convert_str_to_datetime(date, time_amount)

        self.assertEqual(result.hour, 12)
        self.assertEqual(result.day, 11)
        self.assertEqual(result.month, 4)
        self.assertEqual(result.year, 2001)

    def test_convert_str_to_datetime_super_failure(self):
        first_datetime = datetime.now()
        date = "2001-99-99"
        time_amount = "99:99"
        time.sleep(0.1)
        result = convert_str_to_datetime(date, time_amount)
        time.sleep(0.1)
        second_datetime = datetime.now()

        self.assertTrue(first_datetime < result)
        self.assertTrue(second_datetime > result)

    def test_convert_list_to_comma_seperated_string(self):
        test_data = ["one", "two", "three"]
        result = convert_list_to_comma_seperated_string(test_data)

        self.assertEqual("one,two,three", result)

    def test_convert_comma_seperated_string_to_list_singular(self):
        test_data = "hello there"
        result = convert_comma_seperated_string_to_list(test_data)

        self.assertEqual(test_data, result[0])
        self.assertEqual(1, len(result))

    def test_convert_comma_seperated_string_to_list_normal(self):
        test_data = "hello there,whats up,,this is a test"
        result = convert_comma_seperated_string_to_list(test_data)

        self.assertEqual(3, len(result))
        self.assertEqual("hello there", result[0])
        self.assertEqual("whats up", result[1])
        self.assertEqual("this is a test", result[2])
