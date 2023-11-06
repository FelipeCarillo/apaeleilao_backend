from enum import Enum


class STATUS_AUCTION_ENUM(Enum):
    """
    PENDING: The auction is waiting to start
    OPEN: The auction is open
    CLOSED: The auction is closed
    AVAILABLE: The auction is available to reopen
    """

    PENDING = 'PENDING'
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    AVAILABLE = 'AVAILABLE'


class STATUS_AUCTION_PAYMENT_ENUM(Enum):
    """
    PENDING: The auction is closed and the payment is pending
    PAID: The auction is closed and the payment is paid
    EXPIRED: The auction is closed and the payment is expired
    """

    PENDING = 'PENDING'
    PAID = 'PAID'
    EXPIRED = 'EXPIRED'


class PAYMENT_SERVICES(Enum):
    """
    MERCADO_PAGO: Mercado Pago API
    """
    MERCADO_PAGO = 'MERCADO_PAGO'
