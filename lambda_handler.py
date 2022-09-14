from data.provider.DBConfigurationProvider import DBConfigurationProvider
from data.provider.UserRoleProvider import UserRoleProvider
from database.DatabaseConnectionHelper import DatabaseConnectionHelper
from database.MySQLQueryExecutor import MySQLQueryExecutor
# from lambda_event import LambdaEvent
from helper.LoggingHelper import LoggingHelper
from response.ResponseCreator import ResponseCreator
# from response.SetResponses import SetResponses
# from routing.endpoint_router import EndpointRouter
# from security.UserAuthoriser import UserAuthorizer
# from security.exceptions.AuthError import AuthError

logger = LoggingHelper("Handler").retrieve_logger()


def handle(context, event):
    global current_user_id
    # logger.info("Handling")

    # create_db_beta = """CREATE DATABASE meetingsassistant"""
    #
    # initial_sql_setup = """CREATE TABLE meetingsassistant.users (
    # UserId varchar(255) PRIMARY KEY NOT NULL,
    # RoleName varchar(255) NOT NULL);"""
    #
    update_with_inital_user = """INSERT into meetingsassistant.users (UserId, RoleName)
    VALUES ('624c0fe938bf3900699ac5cc', 'role:admin');"""

    update_with_user = """INSERT into meetingsassistant.users (UserId, RoleName)
        VALUES ('624c117bb407b20069e31c01', 'role:standard');"""

    # select_tables = """SELECT * FROM meetingsassistant.users"""

    # db_connection = DatabaseConnectionHelper()

    db_config = DBConfigurationProvider().get_configuration()
    connection_helper = DatabaseConnectionHelper(db_config)

    if connection_helper.is_connection_open():
        query_helper = MySQLQueryExecutor(connection_helper.get_connection_cursor())
        # query_helper.execute_query(create_db_beta)
        # query_helper.execute_query(initial_sql_setup)
        query_helper.execute_query(update_with_inital_user)
        query_helper.execute_query(update_with_user)

    connection_helper.commit_connection()
    connection_helper.close_connection()

    # Authenticate User

    # lambda_event = LambdaEvent(event)
    #
    # try:
    #     user = UserAuthorizer(lambda_event.get_header()).authorise_user()
    # except AuthError as e:
    #     logger.error(e)
    #     return SetResponses.UNAUTHENTICATED
    #
    # # Route request to desired endpoint
    # endpoint_router = EndpointRouter(user, lambda_event.get_request_path(), lambda_event.get_query_parameters())
    # endpoint_response = endpoint_router.route_endpoint()

    retrieve_rows = UserRoleProvider('624c0fe938bf3900699ac5cc')
    logger.debug(retrieve_rows.get_user_role())
    retrieve_rows.finish()

    retrieve_rows_two = UserRoleProvider('624c117bb407b20069e31c01')
    logger.debug(retrieve_rows.get_user_role())
    retrieve_rows_two.finish()

    # Verify user and then call endpoint router. Take result and return it in a formatted model

    return ResponseCreator({"message": "Complete"}).generate_successful_response()
