from abc import ABC
from typing import List

import pytest

from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM
from src.shared.errors.modules_errors import *


class Auction(ABC):
    auction_id: str
    user_id: str
    title: str
    description: str
    images: List[str]
    initial_value: float
    current_value: float
    status: STATUS_AUCTION_ENUM
    date_start: int
    date_end: int
    bids: list
    created_at: int
    AUCTION_ID_LENGTH: 36
    USER_ID_LENGTH: 36
    TITLE_LENGTH: 100
    DESCRIPTION_LENGTH: 300

    def __init__(self, auction_id: str, user_id: str, title: str, description: str, initial_value: float,
                 current_value: float, status: STATUS_AUCTION_ENUM, date_start: int, date_end: int, bids: list,
                 created_at: int):

        self.auction_id = self.validate_and_set_auction_id(auction_id)
        self.user_id = self.validate_and_set_user_id(user_id)
        self.title = self.validate_and_set_title(title)
        self.description = self.validate_and_set_description(description)
        self.initial_value = self.validate_and_set_initial_value(initial_value)
        self.current_value = self.validate_and_set_current_value(current_value)
        self.status = self.validate_and_set_status(STATUS_AUCTION_ENUM(status))
        self.date_start = self.validate_and_set_date_start(date_start)
        self.date_end = self.validate_and_set_date_end(date_end)
        self.bids = self.validate_and_set_bids(bids)
        self.created_at = self.validate_and_set_created_at(created_at)

    def to_dict(self):
        return {
            "auction_id": self.auction_id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "initial_value": self.initial_value,
            "current_value": self.current_value,
            "status": self.status,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "bids": self.bids,
            "created_at": self.created_at
        }

    @staticmethod
    def validate_and_set_auction_id(auction_id: str) -> str or None:
        if auction_id is None:
            raise MissingParameter("auction_id")
        if type(auction_id) != str:
            raise InvalidParameter("auction_id", "deve ser str")
        if len(auction_id) != Auction.AUCTION_ID_LENGTH:
            raise InvalidParameter("auction_id", "deve ter 36 caracteres")
        return auction_id

    @staticmethod
    def validate_and_set_user_id(user_id: str) -> str or None:
        if user_id is None:
            raise MissingParameter("user_id")
        if type(user_id) != str:
            raise InvalidParameter("user_id", "deve ser str")
        if len(user_id) != Auction.USER_ID_LENGTH:
            raise InvalidParameter("user_id", "deve ter 36 caracteres")
        return user_id

    @staticmethod
    def validate_and_set_title(title: str) -> str or None:
        if title is None:
            raise MissingParameter("title")
        if type(title) != str:
            raise InvalidParameter("title", "deve ser str")
        if len(title) != Auction.TITLE_LENGTH:
            raise InvalidParameter("title", "deve ter 100 caracteres")
        return title

    @staticmethod
    def validate_and_set_description(description: str) -> str or None:
        if description is None:
            raise MissingParameter("description")
        if type(description) != str:
            raise InvalidParameter("description", "deve ser str")
        if len(description) != Auction.DESCRIPTION_LENGTH:
            raise InvalidParameter("description", "deve ter 300 caracteres")
        return description

    @staticmethod
    def validate_and_set_initial_value(inital_value: float) -> float or None:
        if inital_value is None:
            return None
        if type(inital_value) != float:
            raise InvalidParameter("inital_values", "deve ser float")
        return inital_value

    @staticmethod
    def validate_and_set_current_value(current_value: float) -> float or None:
        if current_value is None:
            return None
        if type(current_value) != float:
            raise InvalidParameter("current_value", "deve ser float")
        return current_value

    @staticmethod
    def validate_and_set_status(status: STATUS_AUCTION_ENUM):
        if status is None:
            raise MissingParameter("status")
        if type(status) != STATUS_AUCTION_ENUM:
            raise InvalidParameter("status", "deve ser STATUS_AUCTION_ENUM")
        return status

    @staticmethod
    def validate_and_set_date_start(date_start: int) -> int or None:
        if date_start is None:
            return None
        if type(date_start) != int:
            raise InvalidParameter("date_start", "deve ser int")
        return date_start

    @staticmethod
    def validate_and_set_date_end(date_end: int) -> int or None:
        if date_end is None:
            return None
        if type(date_end) != int:
            raise InvalidParameter("date_end", "deve ser int")
        return date_end

    @staticmethod
    def validate_and_set_bids(bids: list) -> int or None:
        if bids is None:
            return None
        if type(bids) != list:
            raise InvalidParameter("bids", "deve ser list")
        return bids

    @staticmethod
    def validate_and_set_created_at(created_at: int) -> int or None:
        if created_at is None:
            return None
        if type(created_at) != int:
            raise InvalidParameter("created_at", "deve ser int")
        return created_at
