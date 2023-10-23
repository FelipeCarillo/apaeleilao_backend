from abc import ABC
from decimal import Decimal

from src.shared.errors.modules_errors import InvalidParameter


class Bid(ABC):
    bid_id: str
    user_id: str
    auction_id: str
    amount: float
    create_at: int

    def __int__(self, bid_id: str, user_id: str, auction_id: str, amount: float, create_at: int):
        self.bid_id = self.validated_and_set_bid_id(bid_id)
        self.user_id = self.validated_and_set_user_id(user_id)
        self.auction_id = self.validated_and_set_auction_id(auction_id)
        self.amount = self.validated_and_set_amount(amount)
        self.create_at = self.validated_and_set_create_at(create_at)

    def to_dict(self):
        return {
            'bid_id': self.bid_id,
            'user_id': self.user_id,
            'auction_id': self.auction_id,
            'amount': float(self.amount),
            'create_at': self.create_at
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
    def validated_and_set_auction_id(auction_id: str) -> str:
        if not auction_id:
            raise InvalidParameter('auction_id', 'é obrigatório')
        if not isinstance(auction_id, str):
            raise InvalidParameter('auction_id', 'deve ser str')
        return auction_id

    @staticmethod
    def validated_and_set_amount(amount: float) -> float:
        if not amount:
            raise InvalidParameter('amount', 'is required')
        if not isinstance(amount, float):
            raise InvalidParameter('amount', 'must be a float')
        amount = round(amount, 2)
        return amount

    @staticmethod
    def validated_and_set_create_at(create_at: int) -> int:
        if not create_at:
            raise InvalidParameter('create_at ', 'é obrigatório')
        if not isinstance(create_at, int):
            raise InvalidParameter('create_at', 'deve ser int')
        return create_at
