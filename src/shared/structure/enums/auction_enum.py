from enum import Enum


class STATUS_AUCTION_ENUM(Enum):
    """
    Enum for auction status. \n
    - **ACTIVE**: Auction active.
    - **CANCEL**: Auction cancel by admin.
    - **ENDED**: Auction ended.
    """

    ACTIVE = 'ACTIVE'
    CANCEL = 'CANCEL'
    ENDED = 'ENDED'