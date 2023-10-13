from typing import Dict, List

from src.shared.errors.modules_errors import InvalidParameter
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



