from data.provider.UserRoleProvider import UserRoleProvider


def handle(context, event):
    print("Handling From")

    initial_sql_setup = """CREATE TABLE betameetingsassistant.users (
    UserId varchar(255) PRIMARY KEY NOT NULL,
    RoleName varchar(255) NOT NULL);"""

    update_with_inital_user = """INSERT into betameetingsassistant.users (UserId, RoleName)
    VALUES ('auth0|621694e858c5f70069b7cb06', 'role:admin');"""

    select_tables = """SELECT * FROM betameetingsassistant.users"""

    # db_connection = DatabaseConnectionHelper()

    retrieve_rows = UserRoleProvider('auth0|621694e858c5f70069b7cb06')
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
