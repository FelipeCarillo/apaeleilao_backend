from typing import List, Optional

from src.shared.errors.modules_errors import *
from src.shared.structure.entities.bid import Bid
from src.shared.structure.entities.payment import Payment
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM


class Auction:
    auction_id: str
    titte: str
    description: str
    start_date: int
    end_date: int
    start_amount: float
    current_amount: float
    bids: List[Optional[Bid]]
    payments: List[Optional[Payment]]
    images: List[str]
    status_auction: STATUS_AUCTION_ENUM
    create_at: int
    AUCTION_ID_LENGTH = 36
    TITTLE_MAX_LENGTH = 100
    TITTLE_MIN_LENGTH = 3
    DESCRIPTION_MAX_LENGTH = 350
    DESCRIPTION_MIN_LENGTH = 5

    def __init__(self, auction_id: str,
                 tittle: str,
                 description: str = None,
                 start_date: int = None,
                 end_date: int = None,
                 start_amount: float = None,
                 current_amount: float = None,
                 bids: List[Optional[Bid]] = None,
                 payments: List[Optional[Payment]] = None,
                 images: List[str] = None,
                 status_auction: STATUS_AUCTION_ENUM = None,
                 create_at: int = None,
                 ):

        self.auction_id = self.validate_and_set_auction_id(auction_id)
        self.tittle = self.validate_and_set_tittle(tittle)
        self.description = self.validate_and_set_description(description)
        self.start_date = self.validate_set_start_date(start_date)
        self.end_date = self.validate_set_end_date(end_date)
        self.start_price = self.validate_and_set_amount(start_amount)
        self.current_amount = self.validate_and_set_amount(current_amount)
        self.bids = self.validate_and_set_bids(bids)
        self.payments = self.validate_and_set_payments(payments)
        self.images = self.validate_and_set_images(images)
        self.status_auction = self.validate_and_set_status_auction(STATUS_AUCTION_ENUM(status_auction))
        self.create_at = self.validate_and_set_create_at(create_at)

    def to_dict(self):
        return {
            "auction_id": self.auction_id,
            "tittle": self.tittle,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "start_price": self.start_price,
            "current_amount": self.current_amount,
            "bids": [bid.to_dict() for bid in self.bids] if len(self.bids) > 0 else [],
            "payments": [payment.to_dict() for payment in self.payments] if len(self.payments) > 0 else [],
            "images": self.images,
            "status_auction": self.status_auction.value,
            "create_at": self.create_at
        }

    @staticmethod
    def validate_and_set_auction_id(auction_id: str) -> str or None:
        if auction_id is None:
            raise MissingParameter("auction_id")
        if type(auction_id) is not str:
            raise InvalidParameter("auction_id", "deve ser uma str")
        if len(auction_id) != Auction.AUCTION_ID_LENGTH:
            raise InvalidParameter("auction_id", "deve ter 36 caracteres")
        return auction_id

    @staticmethod
    def validate_and_set_tittle(tittle: str) -> str or None:
        if tittle is None:
            raise MissingParameter("tittle")
        if Auction.TITTLE_MIN_LENGTH > len(tittle) or len(tittle) > Auction.TITTLE_MAX_LENGTH:
            raise InvalidParameter(
                "tittle",
                f"deve ter no mínimo {Auction.TITTLE_MIN_LENGTH} caracteres e no máximo {Auction.TITTLE_MAX_LENGTH}")
        if type(tittle) != str:
            raise InvalidParameter("tittle", "deve ser uma str")
        return tittle

    @staticmethod
    def validate_and_set_description(description: str) -> str or None:
        if description is None:
            return None
        if Auction.DESCRIPTION_MIN_LENGTH >= len(description) or len(description) >= Auction.DESCRIPTION_MAX_LENGTH:
            raise InvalidParameter(
                "description",
                f"deve ter no mínimo {Auction.DESCRIPTION_MIN_LENGTH} caracteres e no máximo {Auction.DESCRIPTION_MAX_LENGTH}")
        if type(description) != str:
            raise InvalidParameter("description", "deve ser uma str")
        return description

    @staticmethod
    def validate_set_start_date(start_date: int) -> int:
        if start_date is None:
            raise MissingParameter("start_date")
        if type(start_date) != int:
            raise InvalidParameter("start_date", "deve ser um int")
        return start_date

    @staticmethod
    def validate_set_end_date(end_date: int) -> int:
        if end_date is None:
            raise MissingParameter("end_date")
        if type(end_date) != int:
            raise InvalidParameter("end_date", "deve ser um int")
        return end_date

    @staticmethod
    def validate_and_set_amount(start_amount: float) -> float:
        if start_amount is None:
            raise MissingParameter("start_price")
        if type(start_amount) != float:
            raise InvalidParameter("start_price", "deve ser um float")
        return start_amount

    @staticmethod
    def validate_and_set_images(images: List[str]) -> List[str] or List[None]:
        if images is None:
            return []
        if isinstance(images, list):
            raise InvalidParameter("images", "deve ser uma lista")
        for image in images:
            if not isinstance(image, str):
                raise InvalidParameter("images", "deve ser uma lista de str")
        return images

    @staticmethod
    def validate_and_set_status_auction(status_auction: STATUS_AUCTION_ENUM) -> STATUS_AUCTION_ENUM or None:
        if status_auction is None:
            raise MissingParameter("status_auction")
        if type(status_auction) != STATUS_AUCTION_ENUM:
            raise InvalidParameter("status_auction", "deve ser um STATUS_AUCTION_ENUM")
        return status_auction

    @staticmethod
    def validate_and_set_create_at(create_at: int) -> int or None:
        if create_at is None:
            raise MissingParameter("create_at")
        if type(create_at) != int:
            raise InvalidParameter("create_at", "deve ser um int")
        return create_at

    @staticmethod
    def validate_and_set_bids(bids: List[Optional[Bid]]) -> List[Optional[Bid]] or None:
        if bids is None:
            raise MissingParameter("bids")
        if not isinstance(bids, list):
            raise InvalidParameter("bids", "deve ser uma lista")
        if len(bids) > 0:
            for bid in bids:
                if not isinstance(bid, Bid):
                    raise InvalidParameter("bids", "deve ser uma lista de Bid")
        return bids

    @staticmethod
    def validate_and_set_payments(payments: List[Optional[Payment]]) -> List[Optional[Payment]] or None:
        if payments is None:
            raise MissingParameter("payments")
        if not isinstance(payments, list):
            raise InvalidParameter("payments", "deve ser uma lista")
        if len(payments) > 0:
            for payment in payments:
                if not isinstance(payment, Payment):
                    raise InvalidParameter("payments", "deve ser uma lista de Payment")
        return payments
