from abc import ABC, abstractmethod
from typing import Optional, Dict

from src.shared.structure.entities.auction import Auction


class AuctionInterface(ABC):
    @abstractmethod
    def create_auction(self, auction: Auction) -> Dict or None:
        pass

    @abstractmethod
    def get_all_auctions(self, exclusive_start_key: str, amount: int) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_all_auctions_menu(self) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_auction_by_id(self, auction_id: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def update_auction(self, auction: Auction) -> Optional[Dict]:
        pass
