from typing import Dict

from database import Database
from src.shared.structure.entities.auction import Auction
from src.shared.structure.interface.auction_interface import AuctionInterface


class AuctionDynamodb(AuctionInterface):
    def __init__(self):
        self.__dynamodb = Database().get_table_auction()
        self.__dynamodb_user = Database().get_table_user()

    def create_auction(self, auction: Auction) -> Dict or None:
        pass

    def get_all_auctions(self, exclusive_start_key: str = None, limit: int = None) -> Dict or None:
        pass



