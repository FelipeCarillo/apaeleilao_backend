from typing import Dict

from src.shared.structure.entities.user import Auction
from src.shared.structure.interface.auction_interface import AuctionInterface
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM

class GetAllAuctionsMenuUseCase:
    def __init__(self, auction_interface: AuctionInterface):
        self.__auction_interface = auction_interface

    def __call__(self) -> Dict:
        auctions = self.__auction_interface.get_all_auctions_menu()

        if not auctions:
            return None
       
        auctions = [Auction(
            auction_id=auction["auction_id"],
            created_by=auction.get("created_by"),
            title=auction.get("title"),
            description=auction.get("description"),
            date_start=int(auction.get("date_start")) if auction.get("date_start") else None,
            date_end=int(auction.get("date_end")) if auction.get("date_end") else None,
            start_amount=float(auction.get("start_amount")) if auction.get("start_amount") else None,
            current_amount=float(auction.get("current_amount")) if auction.get("current_amount") else None,
            images=auction.get("images"),
            status_auction=STATUS_AUCTION_ENUM(auction.get("status_auction")) if auction.get("status_auction") else None,
            created_at=int(auction.get("created_at")) if auction.get("created_at") else None
        ) for auction in auctions]

        return [auction.to_dict() for auction in auctions]


