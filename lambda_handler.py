# from data.provider.DBConfigurationProvider import DBConfigurationProvider
# from data.provider.UserRoleProvider import UserRoleProvider
# from database.DatabaseConnectionHelper import DatabaseConnectionHelper
# from database.MySQLQueryExecutor import MySQLQueryExecutor
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

    # create_db_beta = """CREATE DATABASE meetingsassistant"""
    #
    # initial_sql_setup = """CREATE TABLE meetingsassistant.meetings (
    # UserId varchar(255) PRIMARY KEY NOT NULL,
    # MeetingDateTime DATETIME NOT NULL,
    # NumberOfAttendees INT NOT NULL,
    # MeetingNotes LONGTEXT,
    # MeetingTitle TEXT NOT NULL,
    # Attendees LONGTEXT NOT NULL);"""
    #
    # update_with_inital_user = """INSERT into meetingsassistant.users (UserId, RoleName)
    # VALUES ('624c0fe938bf3900699ac5cc', 'role:admin');"""
    #
    # update_with_user = """INSERT into meetingsassistant.users (UserId, RoleName)
    #     VALUES ('624c117bb407b20069e31c01', 'role:standard');"""

    # select_tables = """SELECT * FROM meetingsassistant.users"""

    # db_connection = DatabaseConnectionHelper()
    #
    # db_config = DBConfigurationProvider().get_configuration()
    # connection_helper = DatabaseConnectionHelper(db_config)
    #
    # if connection_helper.is_connection_open():
    #     query_helper = MySQLQueryExecutor(connection_helper.get_connection_cursor())
    #     # query_helper.execute_query(create_db_beta)
    #     # query_helper.execute_query(initial_sql_setup)
    #     query_helper.execute_query(initial_sql_setup)
    #
    # connection_helper.commit_connection()
    # connection_helper.close_connection()

    # TODO: Remove
    logger.info(event)

    # Gather event information
    try:
        lambda_event = LambdaEvent(event)
    except InvalidHeaderException as e:
        logger.error("Invalid event: " + str(e))
        return SetResponses.INVALID_REQUEST

    # Authenticate User
    try:
        user = UserAuthorizer(lambda_event.get_header()).authorise_user()
    except AuthError as e:
        logger.error(e)
        return SetResponses.UNAUTHENTICATED

    # Route request to desired endpoint
    endpoint_executor = EndpointExecutor(user, lambda_event.get_query_parameters())
    endpoint_router = EndpointRouter(endpoint_executor, lambda_event.get_request_path())
    return endpoint_router.route_endpoint()
    #
    # retrieve_rows = UserRoleProvider('624c0fe938bf3900699ac5cc')
    # logger.debug(retrieve_rows.get_user_role())
    # retrieve_rows.finish()
    #
    # retrieve_rows_two = UserRoleProvider('624c117bb407b20069e31c01')
    # logger.debug(retrieve_rows.get_user_role())
    # retrieve_rows_two.finish()

    # Verify user and then call endpoint router. Take result and return it in a formatted model

    # return ResponseCreator({"message": "Complete"}).generate_successful_response()
