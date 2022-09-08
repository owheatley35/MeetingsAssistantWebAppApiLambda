import re

from Constants import STRING_SPLITTER

# Regex patterns
USER_ID_PATTERN = re.compile("^([a-z0-9]*)$")
SCRIPT_TAG_PATTERN = re.compile("<script>.*</script>")


# Meetings validation
def validate_user_id(user_id: str) -> bool:
    """
    Validates that user id meets eligibility criteria for database.
    :param user_id: string containing the user id from Auth0
    :return: boolean whether user id is compliant
    """
    return isinstance(user_id, str) and USER_ID_PATTERN.match(user_id) and (len(user_id) <= 255)


def validate_meeting_id(meeting_id) -> bool:
    """
    Validate the meeting id against the database requirements
    :param meeting_id: int unique identifier of the meeting
    :return: boolean whether meeting id is compliant for the database
    """
    return isinstance(meeting_id, int) and meeting_id > 0


def validate_input_string(meeting_note: str) -> bool:
    """
    Validate any string being added to the database.
    :param meeting_note: string to be validated
    :return: boolean whether string is valid
    """
    return isinstance(meeting_note, str) and (len(SCRIPT_TAG_PATTERN.findall(meeting_note)) == 0)


def validate_meeting_note(meeting_note: str) -> bool:
    """
    Validates a meeting note to be added to the database.
    :param meeting_note: note string to be added.
    :return: boolean whether note is valid for database input
    """
    return validate_sql_longtext(meeting_note) and (STRING_SPLITTER not in meeting_note)


def validate_sql_text(text: str) -> bool:
    """
    Validates data for input into a TEXT datatype field in the database.
    :param text: Text string to be added to the database
    :return: boolean whether text is valid to be inserted into the database
    """
    return validate_input_string(text) and (len(text.encode('utf-8')) < 65535)


def validate_sql_longtext(long_text: str) -> bool:
    """
    Validates data for input into a LONGTEXT datatype field in the database
    :param long_text: LONGTEXT string to be added to the database
    :return: boolean whether test is valid to be inserted into the database
    """
    return validate_input_string(long_text) and (len(long_text.encode('utf-8')) < 4294967295)
