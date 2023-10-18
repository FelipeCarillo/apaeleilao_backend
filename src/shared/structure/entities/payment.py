from src.shared.errors.modules_errors import InvalidParameter
from src.shared.structure.entities.user import User
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_PAYMENT_ENUM


class Payment:
    payment_id: str
    user_id: str
    auction_id: str
    amount: float
    date_payment: int
    payment_expires_at: int or None
    status_payment: STATUS_AUCTION_PAYMENT_ENUM

    def __init__(self, price: float = None,
                 payment_expires_at: int = None,
                 status: STATUS_AUCTION_PAYMENT_ENUM = None,
                 voucher: str = None
                 ):
        self.price = self.validate_and_set_price(price)
        self.payment_expires_at = self.validate_and_set_payment_expires_at(payment_expires_at)
        self.status = self.validate_and_set_status(STATUS_AUCTION_PAYMENT_ENUM(status))
        self.voucher = self.validate_and_set_voucher(voucher)

    def to_dict(self):
        return {
            'price': self.price,
            'payment_expires_at': self.payment_expires_at,
            'status': self.status.value,
            'voucher': self.voucher
        }

    @staticmethod
    def validate_and_set_price(price: float) -> float:
        if not price:
            raise InvalidParameter('price', 'is required')
        if not isinstance(price, float):
            raise InvalidParameter('price', 'must be a float')
        return price

    @staticmethod
    def validate_and_set_payment_expires_at(payment_expires_at: int) -> int or None:
        if not payment_expires_at:
            return None
        if not isinstance(payment_expires_at, int):
            raise InvalidParameter('payment_expires_at', 'must be a int')
        return payment_expires_at

    @staticmethod
    def validate_and_set_status(status: STATUS_AUCTION_PAYMENT_ENUM) -> STATUS_AUCTION_PAYMENT_ENUM:
        if not status:
            raise InvalidParameter('status', 'is required')
        if not isinstance(status, STATUS_AUCTION_PAYMENT_ENUM):
            raise InvalidParameter('status', 'must be a STATUS_AUCTION_PAYMENT_ENUM')
        return status

    @staticmethod
    def validate_and_set_voucher(voucher: str) -> str or None:
        if not voucher:
            return None
        if not isinstance(voucher, str):
            raise InvalidParameter('voucher', 'must be a str')
        return voucher
