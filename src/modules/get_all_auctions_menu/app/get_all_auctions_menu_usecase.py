from typing import Dict, Optional

from src.shared.structure.entities.auction import Auction
from src.shared.structure.interface.auction_interface import AuctionInterface
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM


class GetAllAuctionsMenuUseCase:
    def __init__(self, auction_interface: AuctionInterface):
        self.__auction_interface = auction_interface

    def __call__(self) -> Optional[Dict]:
        auctions = self.__auction_interface.get_all_auctions_menu()

        if not auctions:
            return None

        auctions = [Auction(
            auction_id=auction["auction_id"],
            created_by=auction.get("created_by"),
            title=auction.get("title"),
            description=auction.get("description"),
            start_date=int(auction.get("start_date")),
            end_date=int(auction.get("end_date")),
            start_amount=float(auction.get("start_amount")),
            current_amount=float(auction.get("current_amount")),
            images=auction.get("images"),
            status_auction=STATUS_AUCTION_ENUM(auction.get("status_auction")),
            create_at=int(auction.get("created_at"))
        ) for auction in auctions]

        return {auctions: [auction.to_dict() for auction in auctions]}
