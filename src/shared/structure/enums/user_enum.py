from enum import Enum


class STATUS_USER_ACCOUNT_ENUM(Enum):
    """
    Enum for user account status. \n
    - **ACTIVE**: Account is active.
    - **SUSPENDED**: Account is suspended by Admin.
    - **DELETED**: Account is deleted by User.
    - **PENDING**: Account is pending email verification.
    - **BANED**: Account is suspended by Admin.
    """

    ACTIVE = 'ACTIVE'
    SUSPENDED = 'SUSPENDED'
    DELETED = 'DELETED'
    PENDING = 'PENDING'
    BANED = 'BANED'


class TYPE_ACCOUNT_ENUM(Enum):
    """
    Enum for user account type. \n
    - **ADMIN**: Account is admin.
    - **USER**: Account is user.
    """

    ADMIN = 'ADMIN'
    MODERATOR = 'MODERATOR'
    USER = 'USER'






