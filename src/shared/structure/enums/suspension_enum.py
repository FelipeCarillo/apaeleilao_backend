from enum import Enum


class STATUS_SUSPENSION_ENUM(Enum):
    """
    Enum for suspension status. \n
    - **ACTIVE**: Suspension active.
    - **CANCEL**: Suspension cancel by admin.
    - **ENDED**: Suspension ended.
    """

    ACTIVE = 'ACTIVE'
    CANCEL = 'CANCEL'
    ENDED = 'ENDED'
