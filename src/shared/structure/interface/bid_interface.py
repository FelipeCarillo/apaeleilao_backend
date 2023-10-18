from typing import Dict
from abc import ABC, abstractmethod

from src.shared.structure.entities.bid import Bid


class BidInterface(ABC):
    @abstractmethod
    def create_bid(self, bid: Bid) -> Dict or None:
        pass

    @abstractmethod
    def get_all_bid_by_auction(self, auction_id: str) -> Dict or None:
        pass

    @abstractmethod
    def get_bid_by_user_id(self, user_id: str) -> Dict or None:
        pass

    @abstractmethod
    def get_bid_by_id(self, bid_id: str) -> Dict or None:
        pass
