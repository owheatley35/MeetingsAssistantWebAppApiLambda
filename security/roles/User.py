from security.exceptions.AuthError import AuthError
from security.roles.RoleConfiguration import role_configuration
from security.roles.RoleType import RoleType


class User:
    """
    Class to model a user of the application.
    """

    def __init__(self, user_id: str, role_type: str):
        """
        :param user_id: string containing the user id
        :param role_type: RoleType enum containing the role type
        """
        self._user_id: str = user_id

        try:
            self._role_type: RoleType = RoleType(role_type)
        except Exception:
            raise AuthError("Invalid role type:" + role_type, 401)

    def get_id(self) -> str:
        """
        :return: string containing the user id
        """
        return self._user_id

    def is_authorised(self, permission_to_check: set) -> bool:
        """
        Check if the user is authorised to access the endpoint.

        :param permission_to_check: RolePermission enum to check
        :return: boolean indicating if the user is authorised
        """
        permissions: set = role_configuration.get(self._role_type)
        return {permission.value for permission in permission_to_check}.issubset(permissions)
