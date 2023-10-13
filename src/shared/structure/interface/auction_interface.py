from abc import ABC, abstractmethod
from typing import Optional, Dict


class AuctionInterface(ABC):
    @abstractmethod
    def authenticate(self, email: str, password: str = None, password_hash: str = None) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_all_auctions(self) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_auction_by_id(self, auction_id: str) -> Optional[Dict]:
        pass
