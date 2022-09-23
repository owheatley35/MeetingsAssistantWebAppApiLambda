from data.provider.DBConfigurationProvider import DBConfigurationProvider
from database.DatabaseConnectionHelper import DatabaseConnectionHelper
from database.MySQLQueryExecutor import MySQLQueryExecutor
from routing.EndpointExecutor import EndpointExecutor
from security.exceptions.InvalidHeaderException import InvalidHeaderException
from lambda_event import LambdaEvent
from helper.LoggingHelper import LoggingHelper
from response.SetResponses import SetResponses
from routing.endpoint_router import EndpointRouter
from security.UserAuthoriser import UserAuthorizer
from security.exceptions.AuthError import AuthError

logger = LoggingHelper("Handler").retrieve_logger()


def handle(event, context):
    logger.info("Handling")

    create_db_beta = """CREATE DATABASE meetingsassistant"""

    initial_sql_setup = """CREATE TABLE meetingsassistant.meetings (
    MeetingId INT PRIMARY KEY NOT NULL,
    UserId varchar(255) NOT NULL,
    MeetingDateTime DATETIME NOT NULL,
    NumberOfAttendees INT NOT NULL,
    MeetingNotes LONGTEXT,
    MeetingTitle TEXT NOT NULL,
    Attendees LONGTEXT NOT NULL);"""

    create_users_table = """CREATE TABLE meetingsassistant.users (
    UserId varchar(255) NOT NULL PRIMARY KEY,
    RoleName varchar(255) NOT NULL);"""

    update_with_personal_user = """INSERT into meetingsassistant.users (UserId, RoleName)
    VALUES ('621694e858c5f70069b7cb06', 'role:admin');"""

    update_with_inital_user = """INSERT into meetingsassistant.users (UserId, RoleName)
    VALUES ('624c0fe938bf3900699ac5cc', 'role:admin');"""

    update_with_user = """INSERT into meetingsassistant.users (UserId, RoleName)
        VALUES ('624c117bb407b20069e31c01', 'role:standard');"""

    # select_tables = """SELECT * FROM meetingsassistant.users"""

    alter_statement = """ALTER TABLE meetingsassistant.meetings
    ADD MeetingId INT PRIMARY KEY NOT NULL;"""

    alter_statement_two = """ALTER TABLE meetingsassistant.meetings
    MODIFY UserId varchar(255) NOT NULL;"""

    alter_statement_three = """ALTER TABLE meetingsassistant.meetings
        ALTER COLUMN UserId varchar(255) NOT NULL;"""

    alter_statement_four = """ALTER TABLE meetingsassistant.meetings
    DROP UserId;"""

    alter_statement_five = """ALTER TABLE meetingsassistant.meetings
    ADD UserId varchar(255) NOT NULL;"""

    update_alter_table = """ALTER TABLE meetingsassistant.meetings
    MODIFY MeetingId AUTO_INCREMENT;"""

    db_config = DBConfigurationProvider().get_configuration()
    connection_helper = DatabaseConnectionHelper(db_config)

    if connection_helper.is_connection_open():
        query_helper = MySQLQueryExecutor(connection_helper.get_connection_cursor())
        # query_helper.execute_query(alter_statement)
        # query_helper.execute_query(alter_statement_two)

        if "create_database" in event:
            query_helper.execute_query(create_db_beta)

        if "create_table" in event:
            query_helper.execute_query(initial_sql_setup)

        if "create_users_table" in event:
            query_helper.execute_query(create_users_table)

        if "create_users" in event:
            if "my_admin" in event["create_users"]:
                query_helper.execute_query(update_with_personal_user)
            if "admin" in event["create_event"]:
                query_helper.execute_query(update_with_inital_user)
            if "standard" in event["create_event"]:
                query_helper.execute_query(update_with_user)

        if "alter_meetingid" in event:
            query_helper.execute_query(alter_statement)

        if "alter_userid" in event:
            query_helper.execute_query(alter_statement_two)

        if "alter_userid_two" in event:
            query_helper.execute_query(alter_statement_three)

        if "alter_one" in event:
            query_helper.execute_query(alter_statement_four)

        if "alter_three" in event:
            query_helper.execute_query(alter_statement_five)

        if "increment_change" in event:
            query_helper.execute_query(update_alter_table)

    connection_helper.commit_connection()
    connection_helper.close_connection()

    # TODO: Remove
    logger.info(event)

    # Gather event information
    try:
        lambda_event = LambdaEvent(event)
    except InvalidHeaderException as e:
        logger.error("Invalid event: " + str(e))
        return SetResponses.INVALID_REQUEST.value

    # Authenticate User
    try:
        user = UserAuthorizer(lambda_event.get_header()).authorise_user()
    except AuthError as e:
        logger.error(e)
        return SetResponses.UNAUTHENTICATED.value

    # Route request to desired endpoint
    endpoint_executor = EndpointExecutor(user, lambda_event.get_body())
    endpoint_router = EndpointRouter(endpoint_executor, lambda_event.get_request_path())
    response = endpoint_router.route_endpoint()

    if not response or response == {}:
        logger.error("Invalid Response: " + str(response) + ", replacing with server error")
        return SetResponses.INTERNAL_ERROR.value

    logger.info("Response: " + str(response))
    return response
