from typing import Dict

from boto3.dynamodb.conditions import Key, Attr

from src.shared.database.database import Database
from src.shared.structure.entities.bid import Bid
from src.shared.structure.interface.bid_interface import BidInterface


class BidDynamodb(BidInterface):
    def __int__(self):
        self.__dynamodb = Database().get_table_bid()

    def create_bid(self, bid: Bid) -> Dict or None:
        try:
            bid = bid.to_dict()
            self.__dynamodb.put_item(Item=bid)
            return bid
        except Exception as e:
            raise e

    def get_all_bid_by_auction(self, auction_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.query(
                IndexName='AuctionIdIndex',
                KeyConditionExpression=Key('auction_id').eq(auction_id),
            )
            response = query.get('Items', None)
            return response[0] if response else None
        except Exception as e:
            raise e

    def get_bid_by_user_id(self, user_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.query(
                IndexName='UserIdIndex',
                KeyConditionExpression=Key('user_id').eq(user_id),
            )
            response = query.get('Items', None)
            return response[0] if response else None
        except Exception as e:
            raise e

    def get_bid_by_id(self, bid_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.get_item(Key={'bid_id': bid_id})
            response = query.get('Item', None)
            return response
        except Exception as e:
            raise e
