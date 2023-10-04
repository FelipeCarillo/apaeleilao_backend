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

    @classmethod
    def get_value(cls, value):
        for enum_item in cls:
            if enum_item.value == value:
                return enum_item
        return None






