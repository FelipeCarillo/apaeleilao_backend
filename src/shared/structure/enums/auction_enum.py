from enum import Enum


class STATUS_AUCTION_ENUM(Enum):
    """
    OPEN: The auction is open
    CLOSED: The auction is closed
    SUSPENDED: The auction is suspended
    """

    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    SUSPENDED = 'SUSPENDED'


class STATUS_AUCTION_PAYMENT_ENUM(Enum):
    """
    PENDING: The auction is open and the payment is pending
    PAID: The auction is closed and the payment is paid
    EXPIRED: The auction is closed and the payment is expired
    """

    PENDING = 'PENDING'
    PAID = 'PAID'
    EXPIRED = 'EXPIRED'
