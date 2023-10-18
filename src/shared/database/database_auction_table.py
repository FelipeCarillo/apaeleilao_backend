from typing import Dict

from src.shared.database.database import Database
from src.shared.structure.entities.bid import Bid
from src.shared.structure.interface.auction_interface import AuctionInterface


class AuctionDynamodb(AuctionInterface):
    def __int__(self):
        self.__dynamodb = Database().get_table_auction()

    def create_auction(self, auction: Dict) -> Dict or None:
        try:
            self.__dynamodb.put_item(Item=auction)
            return {
                auction
            }
        except Exception as e:
            raise e

    def create_bid(self, auction_id: str, bid: Bid) -> Dict or None:
        try:
            response = self.__dynamodb.update_item(
                Key={"auction_id": auction_id},
                UpdateExpression="SET bids.#bid_id = :bid",
                ExpressionAttributeNames={
                    '#bid_id': bid.bid_id
                },
                ExpressionAttributeValues={
                    ':bid': bid.to_dict()
                },
                ReturnValues="ALL_NEW"
            )
            updated_auction = response.get('Attributes')
            bids = updated_auction.get('bids')
            best_bid = max(bids, key=lambda x: x['amount'])
            second_best_bid = max(bids, key=lambda x: x['amount'] if x['amount'] != best_bid['amount']
                                                                     and x['user_id'] != best_bid['user_id'] else 0)
            self.__dynamodb.update_item(
                Key={"auction_id": auction_id},
                UpdateExpression="SET best_bid = :best_bid, second_best_bid = :second_best_bid",
                ExpressionAttributeValues={
                    ':best_bid': best_bid,
                    ':second_best_bid': second_best_bid
                },
                ReturnValues="ALL_NEW"
            )

        except Exception as e:
            raise e

    def get_all_bids(self, exclusive_start_key: str = None, limit: int = None) -> Dict or None:
        try:
            query = self.__dynamodb.scan(
                ExclusiveStartKey=exclusive_start_key,
                Limit=limit
            )
            response = query.get('Items', None)
            return response
        except Exception as e:
            raise e

    def get_bid_by_id(self, bid_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.get_item(Key={'bid_id': bid_id})
            response = query.get('Item', None)
            return response
        except Exception as e:
            raise e

    def create_payment(self, payment: Payment) -> Dict or None:

        try:
            payment = payment.to_dict()
            self.__dynamodb.put_item(Item=payment)
            return {
                'body': payment
            }
        except Exception as e:
            raise e

    def get_all_auctions(self, exclusive_start_key: str = None, limit: int = None) -> Dict or None:
        try:
            query = self.__dynamodb.scan(
                ExclusiveStartKey=exclusive_start_key,
                Limit=limit
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
            return {
                'body': auction
            }
        except Exception as e:
            raise e
