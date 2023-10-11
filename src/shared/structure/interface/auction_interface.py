from abc import ABC, abstractmethod
from typing import Optional, Dict

from src.shared.structure.entities.auction import Auction


class AuctionInterface(ABC):

    @abstractmethod
    def authenticate(self, email: str, password: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_all_auctions(self) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_auction_by_id(self, auction_id: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_auction_by_title(self, title: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def create_auction(self, auction: Auction) -> Optional[Dict]:
        pass

    @abstractmethod
    def update_auction(self, auction: Auction) -> Optional[Dict]:
        pass

    @abstractmethod
    def delete_auction(self, auction: Auction) -> Optional[Dict]:
        pass