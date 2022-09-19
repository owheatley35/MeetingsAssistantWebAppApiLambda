from enum import Enum


class RoleType(Enum):
    """
    Enum to model the role types of Users.
    """
    ADMIN = "role:admin"
    STANDARD = "role:standard"
