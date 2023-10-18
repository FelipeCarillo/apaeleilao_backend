from typing import Dict

from src.shared.database.database import Database
from src.shared.structure.entities.bid import Bid
from src.shared.structure.entities.auction import Auction
from src.shared.structure.interface.auction_interface import AuctionInterface


class AuctionDynamodb(AuctionInterface):
    def __init__(self):
        self.__dynamodb = Database().get_table_auction()

    def create_auction(self, auction: Auction) -> Dict or None:
        try:
            auction = auction.to_dict()
            self.__dynamodb.put_item(Item=auction)
            return auction
        except Exception as e:
            raise e

    def get_all_auctions(self, exclusive_start_key: str = None, amount: int = 6) -> Dict or None:
        try:
            if not exclusive_start_key:
                query = self.__dynamodb.scan(
                    Limit=amount,
                    Sortby='created_at',
                    SortOrder='DESC'
                )
                response = query.get('Items', None)
                return response
            query = self.__dynamodb.scan(
                ExclusiveStartKey=exclusive_start_key,
                Limit=amount
            )
            response = query.get('Items', None)
            return response
        except Exception as e:
            raise e

    def get_auction_by_id(self, auction_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.get_item(Key={'auction_id': auction_id})
            response = query.get('Item', None)
            return response
        except Exception as e:
            raise e

    def update_auction(self, auction: Auction) -> Dict or None:
        try:
            auction = auction.to_dict()
            self.__dynamodb.put_item(Item=auction)
            return auction
        except Exception as e:
            raise e
