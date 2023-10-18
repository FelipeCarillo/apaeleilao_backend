from decimal import Decimal

from src.shared.errors.modules_errors import InvalidParameter


class Bid:
    bid_id: str
    auction_id: str
    user_id: str
    amount: float
    date_bid: int

    def __int__(self, bid_id: str, auction_id:str, user_id: str, amount: float, date_bid: int):
        self.bid_id = bid_id
        self.user_id = user_id
        self.amount = self.validated_and_set_amount(amount)
        self.date_bid = date_bid

    def to_dict(self):
        return {
            'bid_id': self.bid_id,
            'user_id': self.user_id,
            'amount': Decimal(self.amount),
            'date_bid': self.date_bid
        }

    @staticmethod
    def validated_and_set_amount(amount: float) -> float:
        if isinstance(amount, str):
            raise InvalidParameter("amount", "deve ser float")
        if amount <= 0:
            raise InvalidParameter('amount', 'deve ser maior que 0')
        return amount
