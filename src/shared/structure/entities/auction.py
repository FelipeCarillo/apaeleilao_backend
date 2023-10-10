from abc import ABC

from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM


class Auction(ABC):
    auction_id: str
    user_id: str
    title: str
    description: str
    initial_value: float
    current_value: float
    status: str
    date_start: int
    date_end: int
    bids: list
    created_at: int

    def __init__(self, auction_id: str, user_id: str, title: str, description: str, initial_value: float,
                    current_value: float, status: STATUS_AUCTION_ENUM, date_start: int, date_end: int, bids: list,
                    created_at: int):




