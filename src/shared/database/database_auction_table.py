from decimal import Decimal
from typing import Dict, List
from boto3.dynamodb.conditions import Key, Attr

from src.shared.database.database import Database
from src.shared.structure.entities.auction import Auction
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM
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

    def get_all_auctions(self, exclusive_start_key: str = None, amount: int = 6) -> List[Dict] or None:
        try:
            if not exclusive_start_key:
                query = self.__dynamodb.scan(
                    Limit=amount,
                )
            else:
                query = self.__dynamodb.scan(
                    ExclusiveStartKey=exclusive_start_key,
                    Limit=amount
                )
            response = query.get('Items', None)
            return response
        except Exception as e:
            raise e

    def get_auctions_menu(self) -> List[Dict] or None:
        try:
            status_permitted = STATUS_AUCTION_ENUM.OPEN.value or STATUS_AUCTION_ENUM.PENDING.value
            query = self.__dynamodb.query(
                IndexName='Status-CreateAt-Index',
                KeyConditionExpression=Key('status_auction').eq(status_permitted),
                ScanIndexForward=True,
                Limit=6
            )
            response = query.get('Items', None)
            return response
        except Exception as e:
            raise e

    def get_auction_between_dates(self, start_date: int, end_date: int) -> List[Dict] or None:
        try:
            status_to_search = STATUS_AUCTION_ENUM.OPEN.value or STATUS_AUCTION_ENUM.PENDING.value
            query = self.__dynamodb.query(
                IndexName='Status-CreateAt-Index',
                KeyConditionExpression=Key('status_auction').eq(status_to_search) & Key('create_at').between(
                    start_date, end_date),
            )
            response = query.get('Items', None)
            return response if len(response) > 0 else None
        except Exception as e:
            raise e

    def get_auction_by_id(self, auction_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.get_item(Key={'auction_id': auction_id})
            response = query.get('Item', None)
            return response
        except Exception as e:
            raise e

    def get_last_auction_id(self) -> int or None:
        try:
            query = self.__dynamodb.scan(
                Limit=1,
                ScanIndexForward=False,
                ProjectionExpression='auction_id'
            )
            response = query.get('Items', None)
            return int(response[0].get('auction_id')) if len(response) > 0 else None
        except Exception as e:
            raise e

    def update_auction_information(self, auction: Auction) -> Dict or None:
        try:
            response = self.__dynamodb.update_item(
                Key={'auction_id': auction.auction_id},
                UpdateExpression='SET tittle = :tittle, description = :description, start_date = :start_date, '
                                 'end_date = :end_date, start_amount = :start_amount, current_amount = '
                                 ':current_amount, images = :images, status_auction = :status_auction',
                ExpressionAttributeValues={
                    ':tittle': auction.tittle,
                    ':description': auction.description,
                    ':start_date': auction.start_date,
                    ':end_date': auction.end_date,
                    ':start_amount': auction.start_price,
                    ':current_amount': auction.current_amount,
                    ':images': auction.images,
                    ':status_auction': auction.status_auction.value
                },
                ReturnValues='UPDATED_NEW'
            )
            return response['Attributes']
        except Exception as e:
            raise e
