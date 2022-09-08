from datetime import datetime
from typing import List

from Constants import STRING_SPLITTER, STRING_DATE_SPLITTER, STRING_TIME_SPLITTER
from helper.LoggingHelper import LoggingHelper

logger = LoggingHelper('StringHelper').retrieve_logger()


def break_string_into_list(list_string: str) -> List[str]:
    """
    Takes a String and converts it into a list via custom seperator

    :param list_string: list with custom seperator
    :return: List of Strings
    """

    logger.info("Breaking String into list")

    if STRING_SPLITTER not in list_string:
        return [list_string]

    temp_list = list_string.split(STRING_SPLITTER)
    del temp_list[0]
    return temp_list


def convert_list_into_string(list_in: List[str]) -> str:
    """
    Converts a list of string into a single string of the items via a custom seperator.

    :param list_in: A list of strings to be formatted
    :return: A single string with all items seperated by the custom string splitter
    """
    return STRING_SPLITTER + STRING_SPLITTER.join(list_in)


def convert_str_to_datetime(meeting_date: str, meeting_time: str) -> datetime:
    """
    Converts a string of date and time into a python datetime object for a database entry.
    :param meeting_date: String of date formatted yyyy-mm-dd
    :param meeting_time: String of time formatted hh:mm
    :return: A python datetime object from the inputted strings
    """

    if STRING_DATE_SPLITTER not in meeting_date and STRING_TIME_SPLITTER not in meeting_time:
        # Raise Exception
        return datetime.now()

    split_date = meeting_date.split(STRING_DATE_SPLITTER)
    split_time = meeting_time.split(STRING_TIME_SPLITTER)

    try:
        year: int = int(split_date[0])
        month: int = int(split_date[1])
        day: int = int(split_date[2])
        hour: int = int(split_time[0])
        mins: int = int(split_time[1])
        return datetime(year, month, day, hour, mins, 0, 0)
    except Exception as e:
        logger.error("Failed to convert string to datetime: %s", e)


def convert_list_to_comma_seperated_string(str_list: List[str]) -> str:
    """
    Converts a list of strings into a comma seperated list in a single string
    :param str_list: List of strings to be placed into cs list
    :return: A string containing a comma seperated list of the items in the list.
    """
    return ",".join(str_list)


def convert_comma_seperated_string_to_list(string: str) -> List[str]:
    """
    Takes a string with a comma seperated list and converts to a List object of string
    :param string: A comma seperated list in a string eg "apples, bananas, oranges"
    :return: A list of strings that were seperated by commas eg ["apples", "bananas", "oranges"]
    """

    if ',' in string:
        string_list = string.split(',')
        stripped_string_list = []

        for item in string_list:
            item.strip()
            stripped_string_list.append(item)

        if "" in stripped_string_list:
            string_list.remove("")

        return string_list
    else:
        return [string.strip()]
