from abc import ABC
from typing import Dict
from decimal import Decimal

from src.shared.errors.modules_errors import InvalidParameter
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_PAYMENT_ENUM


class Payment(ABC):
    payment_id: str
    user_id: str
    amount: Decimal
    created_at: int
    date_payment: int or None
    payment_expires_at: int or None
    status_payment: STATUS_AUCTION_PAYMENT_ENUM

    def __init__(self, payment_id: str, user_id: str, amount: str, created_at: int, date_payment: int or None,
                 payment_expires_at: int or None, status_payment: STATUS_AUCTION_PAYMENT_ENUM):
        self.payment_id = self.validate_and_set_payment_id(payment_id)
        self.user_id = self.validate_and_set_user_id(user_id)
        self.amount = self.validate_and_set_price(amount)
        self.created_at = self.validate_and_set_created_at(created_at)
        self.date_payment = self.validate_and_set_date_payment(date_payment)
        self.payment_expires_at = self.validate_and_set_payment_expires_at(payment_expires_at)
        self.status_payment = self.validate_and_set_status(status_payment)

    def to_dict(self) -> Dict:
        return {
            'payment_id': self.payment_id,
            'user_id': self.user_id,
            'amount': self.amount,
            'created_at': self.created_at,
            'date_payment': self.date_payment,
            'payment_expires_at': self.payment_expires_at,
            'status_payment': self.status_payment.value
        }

    @staticmethod
    def validate_and_set_payment_id(payment_id: str) -> str:
        if not payment_id:
            raise InvalidParameter('payment_id', 'is required')
        if not isinstance(payment_id, str):
            raise InvalidParameter('payment_id', 'must be a str')
        return payment_id

    @staticmethod
    def validate_and_set_user_id(user_id: str) -> str:
        if not user_id:
            raise InvalidParameter('user_id', 'is required')
        if not isinstance(user_id, str):
            raise InvalidParameter('user_id', 'must be a str')
        return user_id

    @staticmethod
    def validate_and_set_amount(amount: str) -> Decimal:
        if not amount:
            raise InvalidParameter('amount', 'is required')
        if not isinstance(amount, str):
            raise InvalidParameter('amount', 'must be a str')
        amount = amount.replace(',', '.')
        if len(amount.split('.')[-1]) > 2:
            raise InvalidParameter('amount', 'must have 2 decimal places')
        return Decimal(amount)

    @staticmethod
    def validate_and_set_created_at(created_at: int) -> int:
        if not created_at:
            raise InvalidParameter('created_at', 'is required')
        if not isinstance(created_at, int):
            raise InvalidParameter('created_at', 'must be a int')
        return created_at

    @staticmethod
    def validate_and_set_date_payment(date_payment: int) -> int or None:
        if not date_payment:
            return None
        if not isinstance(date_payment, int):
            raise InvalidParameter('date_payment', 'must be a int')
        return date_payment

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
