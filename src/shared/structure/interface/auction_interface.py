from abc import ABC, abstractmethod
from typing import Optional, Dict


class AuctionInterface(ABC):
    @abstractmethod
    def create_auction(self, auction: Dict) -> Optional[Dict]:
        pass

    @abstractmethod
    def create_bid(self, auction: str, bid: Dict) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_all_auctions(self, exclusive_start_key: str = None, amount: int = 15) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_auction_by_id(self, auction_id: str) -> Optional[Dict]:
        pass
