from enum import Enum


class STATUS_AUCTION_ENUM(Enum):
    """
    PENDING: The auction is waiting to start
    OPEN: The auction is open
    CLOSED: The auction is closed
    """

    PENDING = 'PENDING'
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'


class STATUS_AUCTION_PAYMENT_ENUM(Enum):
    """
    PENDING: The auction is closed and the payment is pending
    PAID: The auction is closed and the payment is paid
    EXPIRED: The auction is closed and the payment is expired
    """

    PENDING = 'PENDING'
    PAID = 'PAID'
    EXPIRED = 'EXPIRED'
