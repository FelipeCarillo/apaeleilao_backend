from abc import ABC
from typing import List, Optional, Dict

from src.shared.errors.modules_errors import *
from src.shared.structure.entities.bid import Bid
from src.shared.structure.entities.payment import Payment
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM


class Auction(ABC):
    auction_id: str
    created_by: str  # who created the auction user_id
    title: str
    description: str
    start_date: int
    end_date: int
    start_amount: float
    current_amount: float
    images: List[Optional[Dict]]
    status_auction: STATUS_AUCTION_ENUM
    created_at: int
    USER_ID_LENGTH = 36
    TITTLE_MAX_LENGTH = 100
    TITTLE_MIN_LENGTH = 3
    DESCRIPTION_MAX_LENGTH = 350
    DESCRIPTION_MIN_LENGTH = 3

    def __init__(self, auction_id: str,
                 created_by: str,
                 title: str,
                 description: str = None,
                 start_date: int = None,
                 end_date: int = None,
                 start_amount: float = None,
                 current_amount: float = None,
                 images: List[Optional[Dict]] = None,
                 status_auction: str = None,
                 created_at: int = None,
                 ):

        self.auction_id = self.validate_and_set_auction_id(auction_id)
        self.created_by = self.validate_and_set_user_id(created_by)
        self.title = self.validate_and_set_title(title)
        self.description = self.validate_and_set_description(description)
        self.start_date = self.validate_set_start_date(start_date)
        self.end_date = self.validate_set_end_date(end_date)
        self.start_amount = self.validate_and_set_amount(start_amount)
        self.current_amount = self.validate_and_set_amount(current_amount)
        self.images = self.validate_and_set_images(images)
        self.status_auction = self.validate_and_set_status_auction(STATUS_AUCTION_ENUM(status_auction))
        self.created_at = self.validate_and_set_created_at(created_at)

    def to_dict(self):
        return {
            "auction_id": self.auction_id,
            "created_by": self.created_by,
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "start_amount": self.start_amount,
            "current_amount": self.current_amount,
            "images": self.images,
            "status_auction": self.status_auction.value,
            "created_at": self.created_at
        }

    @staticmethod
    def validate_and_set_auction_id(auction_id: str) -> str:
        if auction_id is None:
            raise MissingParameter("auction_id")
        if type(auction_id) is not str:
            raise InvalidParameter("auction_id", "deve ser uma str")
        if not auction_id.isnumeric():
            raise InvalidParameter("auction_id", "deve ser um número")
        return auction_id

    @staticmethod
    def validate_and_set_user_id(user_id: str) -> str:
        if user_id is None:
            raise MissingParameter("user_id")
        if type(user_id) is not str:
            raise InvalidParameter("auction_id", "deve ser uma str")
        if len(user_id) != Auction.USER_ID_LENGTH:
            raise InvalidParameter("auction_id", "deve ter 36 caracteres")
        return user_id

    @staticmethod
    def validate_and_set_title(title: str) -> str:
        if title is None:
            raise MissingParameter("title")
        if Auction.TITTLE_MIN_LENGTH > len(title) or len(title) > Auction.TITTLE_MAX_LENGTH:
            raise InvalidParameter(
                "title",
                f"deve ter no mínimo {Auction.TITTLE_MIN_LENGTH} caracteres e no máximo {Auction.TITTLE_MAX_LENGTH}")
        if isinstance(title, str) is False:
            raise InvalidParameter("title", "deve ser uma str")
        return title

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
    def validate_and_set_amount(amount: float) -> float:
        if amount is None:
            raise MissingParameter("amount")
        if type(amount) != float:
            raise InvalidParameter("amount", "deve ser um número com casas decimais")
        amount = round(amount, 2)
        return amount

    @staticmethod
    def validate_and_set_images(images: List[Optional[Dict]]) -> List[Optional[Dict]]:
        if images is None:
            raise MissingParameter("images")
        if len(images) == 0:
            return []
        if isinstance(images, list) is False:
            raise InvalidParameter("images", "deve ser uma lista")
        for image in images:
            if not isinstance(image, dict):
                raise InvalidParameter("images", "deve ser uma lista de dict")
            if not image.get('image_id'):
                raise MissingParameter("image_id")
            if type(image.get('image_id')) != str:
                raise InvalidParameter("image_id", "deve ser uma str")
            if not image.get('image_body'):
                raise MissingParameter("image_body")
            if type(image.get('image_body')) != str:
                raise InvalidParameter("image_body", "deve ser uma str")
            file_type_permitted = ['png', 'jpg', 'jpeg']
            image_description = image.get('image_body').split(',')[0]
            content_type = image_description.split(':')[1].split(";")[0]
            if content_type.split("/")[-1] not in file_type_permitted:
                raise InvalidParameter("image_body", "deve ser uma imagem png, jpg ou jpeg")
            image['content_type'] = content_type
        return images

    @staticmethod
    def validate_and_set_status_auction(status_auction: STATUS_AUCTION_ENUM) -> STATUS_AUCTION_ENUM or None:
        if status_auction is None:
            raise MissingParameter("status_auction")
        if isinstance(status_auction, STATUS_AUCTION_ENUM) is False:
            raise InvalidParameter("status_auction", "deve ser um STATUS_AUCTION_ENUM")
        return status_auction

    @staticmethod
    def validate_and_set_created_at(created_at: int) -> int or None:
        if created_at is None:
            raise MissingParameter("create_at")
        if isinstance(created_at, int) is False:
            raise InvalidParameter("create_at", "deve ser um int")
        return created_at

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
    def validate_and_set_payments(payments: List[Optional[Payment]]) -> List[Optional[Payment]]:
        if payments is None:
            raise MissingParameter("payments")
        if not isinstance(payments, list):
            raise InvalidParameter("payments", "deve ser uma lista")
        if len(payments) > 0:
            for payment in payments:
                if not isinstance(payment, Payment):
                    raise InvalidParameter("payments", "deve ser uma lista de Payment")
        return payments
