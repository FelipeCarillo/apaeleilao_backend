from abc import ABC

from src.shared.errors.modules_errors import InvalidParameter


class Bid(ABC):
    bid_id: str
    user_id: str
    first_name: str
    auction_id: str
    amount: float
    created_at: int

    def __init__(self, bid_id: str, user_id: str, email: str, first_name: str, auction_id: str, amount: float, created_at: int):
        self.bid_id = self.validated_and_set_bid_id(bid_id)
        self.user_id = self.validated_and_set_user_id(user_id)
        self.email = email
        self.first_name = first_name
        self.auction_id = self.validated_and_set_auction_id(auction_id)
        self.amount = self.validated_and_set_amount(float(amount))
        self.created_at = self.validated_and_set_created_at(created_at)

    def to_dict(self):
        return {
            'bid_id': self.bid_id,
            'user_id': self.user_id,
            'email': self.email,
            'first_name': self.first_name,
            'auction_id': self.auction_id,
            'amount': self.amount,
            'create_at': self.created_at
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
    def validated_and_set_created_at(created_at: int) -> int:
        if not created_at:
            raise InvalidParameter('created_at ', 'é obrigatório')
        if not isinstance(created_at, int):
            raise InvalidParameter('created_at', 'deve ser int')
        return created_at
