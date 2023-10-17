from typing import Dict, List

from src.shared.errors.modules_errors import *
from src.shared.structure.entities.bid import Bid
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM, STATUS_AUCTION_PAYMENT_ENUM


class Auction:
    auction_id: str
    titte: str
    description: str
    start_date: int
    end_date: int
    start_price: float
    current_price: float
    bids: List[Bid]
    status_auction: STATUS_AUCTION_ENUM
    status_payment: STATUS_AUCTION_PAYMENT_ENUM
    AUCTION_ID_LENGTH = 36
    TITTLE_MAX_LENGTH = 100
    TITTLE_MIN_LENGTH = 5
    DESCRIPTION_MAX_LENGTH = 350
    DESCRIPTION_MIN_LENGTH = 10

    def __init__(self, auction_id: str = None,
                 tittle: str = None,
                 description: str = None,
                 start_date: int = None,
                 end_date: int = None,
                 start_price: float = None,
                 current_price: float = None,
                 bids: List[Bid] = None,
                 status_auction: STATUS_AUCTION_ENUM = None,
                 status_payment: STATUS_AUCTION_PAYMENT_ENUM = None):
    
        self.auction_id = self.validate_and_set_auctio_id(auction_id)
        self.tittle = self.validate_and_set_tittle(tittle)
        self.description = self.validate_and_set_description(description)
        self.start_date = self.validate_set_start_date(start_date)
        self.end_date = self.validate_set_end_date(end_date)
        self.start_price = self.validate_and_set_start_price(start_price)
        self.current_price = self.validate_and_set_current_price(current_price)
        self.bids = self.validate_and_set_bids(bids)
        self.status_auction = self.validate_and_set_status_auction(status_auction)
        self.status_payment = self.validate_and_set_status_payment(status_payment)
    
    def to_dict(self):
        return {
            "auction_id": self.auction_id,
            "tittle": self.tittle,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "start_price": self.start_price,
            "current_price": self.current_price,
            "bids": self.bids,
            "status_auction": self.status_auction,
            "status_payment": self.status_payment
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
            raise MissingParameter("description")
        if Auction.DESCRIPTION_MIN_LENGTH > len(description) or len(description) > Auction.DESCRIPTION_MAX_LENGTH:
            raise InvalidParameter(
                "description", 
                f"deve ter no mínimo {Auction.DESCRIPTION_MIN_LENGTH} caracteres e no máximo {Auction.DESCRIPTION_MAX_LENGTH}")
        if type(description) != str:
            raise InvalidParameter("description", "deve ser uma str")
        return description

    @staticmethod
    def validate_set_start_date(start_date: int) -> int or None:
        if start_date is None:
            return None
        if type(start_date) != int:
            raise InvalidParameter("start_date", "deve ser um int")
        return start_date

    @staticmethod
    def validate_set_end_date(end_date: int) -> int or None:
        if end_date is None:
            return None
        if type(end_date) != int:
            raise InvalidParameter("end_date", "deve ser um int")
        return end_date

    @staticmethod
    def validate_and_set_start_price(start_price: float) -> float or None:
        if start_price is None:
            raise MissingParameter("start_price")
        if type(start_price) != float:
            raise InvalidParameter("start_price", "deve ser um float")
        return start_price

    @staticmethod
    def validate_and_set_current_price(current_price: float) -> float or None:
        if current_price is None:
            raise MissingParameter("current_price")
        if type(current_price) != float:
            raise InvalidParameter("current_price", "deve ser um float")
        return current_price

    @staticmethod
    def validate_and_set_bids(bids: List[Bid]) -> List[Bid] or None:
        if bids is None:
            raise MissingParameter("bids")
        if type(bids) != list:
            raise InvalidParameter("bids", "deve ser uma lista")
        return bids

    @staticmethod
    def validate_and_set_status_auction(status_auction: STATUS_AUCTION_ENUM) -> STATUS_AUCTION_ENUM or None:
        if status_auction is None:
            raise MissingParameter("status_auction")
        if type(status_auction) != STATUS_AUCTION_ENUM:
            raise InvalidParameter("status_auction", "deve ser um STATUS_AUCTION_ENUM")
        return status_auction

    @staticmethod
    def validate_and_set_status_payment(status_payment: STATUS_AUCTION_PAYMENT_ENUM) -> STATUS_AUCTION_PAYMENT_ENUM or None:
        if status_payment is None:
            raise MissingParameter("status_payment")
        if type(status_payment) != STATUS_AUCTION_PAYMENT_ENUM:
            raise InvalidParameter("status_payment", "deve ser um STATUS_AUCTION_PAYMENT_ENUM")
        return status_payment



