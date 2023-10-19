from abc import ABC
from decimal import Decimal

from src.shared.errors.modules_errors import InvalidParameter


class Bid(ABC):
    bid_id: str
    user_id: str
    amount: Decimal
    date_bid: int

    def __int__(self, bid_id: str, user_id: str, amount: str, date_bid: int):
        self.bid_id = self.validated_and_set_bid_id(bid_id)
        self.user_id = self.validated_and_set_user_id(user_id)
        self.amount = self.validated_and_set_amount(amount)
        self.date_bid = self.validated_and_set_date_bid(date_bid)

    def to_dict(self):
        return {
            'bid_id': self.bid_id,
            'user_id': self.user_id,
            'amount': self.amount,
            'date_bid': self.date_bid
        }

    @staticmethod
    def validated_and_set_bid_id(bid_id: str) -> str:
        if not bid_id:
            raise InvalidParameter('bid_id', 'é obrigatório')
        if not isinstance(bid_id, str):
            raise InvalidParameter('bid_id', 'deve ser str')
        return bid_id

    @staticmethod
    def validated_and_set_user_id(user_id: str) -> str:
        if not user_id:
            raise InvalidParameter('user_id', 'é obrigatório')
        if not isinstance(user_id, str):
            raise InvalidParameter('user_id', 'deve ser str')
        return user_id

    @staticmethod
    def validated_and_set_amount(amount: str) -> Decimal:
        if not amount:
            raise InvalidParameter('amount', 'é obrigatório')
        if not isinstance(amount, str):
            raise InvalidParameter('amount', 'deve ser str')
        return Decimal(amount)

    @staticmethod
    def validated_and_set_date_bid(date_bid: int) -> int:
        if not date_bid:
            raise InvalidParameter('date_bid', 'é obrigatório')
        if not isinstance(date_bid, int):
            raise InvalidParameter('date_bid', 'deve ser int')
        return date_bid
