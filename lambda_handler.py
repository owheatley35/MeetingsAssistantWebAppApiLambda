from data.provider.DBConfigurationProvider import DBConfigurationProvider
from data.provider.UserRoleProvider import UserRoleProvider
from database.DatabaseConnectionHelper import DatabaseConnectionHelper
from database.MySQLQueryExecutor import MySQLQueryExecutor


def handle(context, event):
    print("Handling From")

    initial_sql_setup = """CREATE TABLE betameetingsassistant.users (
    UserId varchar(255) PRIMARY KEY NOT NULL,
    RoleName varchar(255) NOT NULL);"""

    update_with_inital_user = """INSERT into betameetingsassistant.users (UserId, RoleName)
    VALUES ('621694e858c5f70069b7cb06', 'role:admin');"""

    select_tables = """SELECT * FROM betameetingsassistant.users"""

    # db_connection = DatabaseConnectionHelper()

    db_config = DBConfigurationProvider().get_configuration()
    connection_helper = DatabaseConnectionHelper(db_config)

    if connection_helper.is_connection_open():
        query_helper = MySQLQueryExecutor(connection_helper.get_connection_cursor())
        query_helper.execute_query(initial_sql_setup)
        query_helper.execute_query(update_with_inital_user)

    connection_helper.commit_connection()
    connection_helper.close_connection()


    retrieve_rows = UserRoleProvider('621694e858c5f70069b7cb06')
    print(retrieve_rows.get_user_role())

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "message": "Complete"
        }
    }
