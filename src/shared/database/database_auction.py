from decimal import Decimal
from typing import Dict, List, Optional
from boto3.dynamodb.conditions import Key, Attr

from src.shared.database.database import Database
from src.shared.structure.entities.auction import Auction
from src.shared.structure.entities.bid import Bid
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM
from src.shared.structure.interface.auction_interface import AuctionInterface


class AuctionDynamodb(AuctionInterface):
    def __init__(self):
        self.__dynamodb = Database().get_table_auction()

    def create_auction(self, auction: Auction) -> Dict or None:
        try:
            auction = auction.to_dict()
            auction['_id'] = "AUCTION#" + auction.pop("auction_id")
            auction['start_amount'] = Decimal(str(auction['start_amount']))
            auction['current_amount'] = Decimal(str(auction['current_amount']))
            self.__dynamodb.put_item(Item=auction)
            return auction
        except Exception as e:
            raise e

    def get_all_auctions(self, exclusive_start_key: str = None, amount: int = 6, scan_forward: bool = False,
                         status_to_search: STATUS_AUCTION_ENUM = None) -> List[Dict] or None:
        try:
            exclusive_start_key = "AUCTION#" + exclusive_start_key if exclusive_start_key else None
            get_auction_expression = Key('_id').begins_with('AUCTION#')
            get_status_auction_expression = Attr('status_auction').eq(
                status_to_search.value) if status_to_search else None
            if get_status_auction_expression:
                get_auction_expression = get_auction_expression & get_status_auction_expression

            if not exclusive_start_key:
                query = self.__dynamodb.query(
                    KeyConditionExpression=get_auction_expression,
                    Limit=amount,
                    ScanIndexForward=scan_forward
                )
            else:
                query = self.__dynamodb.query(
                    KeyConditionExpression=get_auction_expression,
                    Limit=amount,
                    ScanIndexForward=scan_forward,
                    ExclusiveStartKey={'_id': exclusive_start_key}
                )
            response = query.get('Items', None)
            if response:
                for auction in response:
                    auction['auction_id'] = auction.pop('_id').replace('AUCTION#', '')
                    auction['start_amount'] = round(float(auction['start_amount']), 2)
                    auction['current_amount'] = round(float(auction['current_amount']), 2)
            return response
        except Exception as e:
            raise e

    def get_all_auctions_menu(self) -> Optional[List[Dict]]:
        try:
            query = self.__dynamodb.query(
                KeyConditionExpression=Key('_id').begins_with('AUCTION#'),
                FilterExpression=Attr('status_auction').eq(STATUS_AUCTION_ENUM.OPEN.value) | Attr('status_auction').eq(STATUS_AUCTION_ENUM.PENDING.value),
                limit=6,
                ScanIndexForward=True
            )
            response = query.get('Items')
            if len(response) > 0:
                for auction in response:
                    auction['auction_id'] = auction.pop('_id').replace('AUCTION#', '')
                    auction['start_amount'] = round(float(auction['start_amount']), 2)
                    auction['current_amount'] = round(float(auction['current_amount']), 2)
            return response if len(response) > 0 else None
        except Exception as e:
            raise e

    def get_auction_between_dates(self, start_date: int, end_date: int) -> List[Dict] or None:
        try:
            status_to_search = STATUS_AUCTION_ENUM.OPEN.value or STATUS_AUCTION_ENUM.PENDING.value
            query = self.__dynamodb.query(
                KeyConditionExpression=Key('_id').begins_with('AUCTION#'),
                FilterExpression=Attr('status_auction').eq(status_to_search) & Attr('start_date').between(start_date, end_date)
            )
            response = query.get('Items', None)
            return response if len(response) > 0 else None
        except Exception as e:
            raise e

    def get_auction_by_id(self, auction_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.query(KeyConditionExpression=Key('_id').eq('AUCTION#' + auction_id)).get('Items', None)
            response = query[0] if query else None
            if response:
                response['auction_id'] = response.pop('_id').replace('AUCTION#', '')
                response['start_amount'] = round(float(response['start_amount']), 2)
                response['current_amount'] = round(float(response['current_amount']), 2)
            return response
        except Exception as e:
            raise e

    def get_last_auction_id(self) -> int or None:
        try:
            query = self.__dynamodb.query(
                KeyConditionExpression=Key('_id').begins_with('AUCTION#'),
                ScanIndexForward=False,
                Limit=1
            )
            response = query.get('Items', None)
            if response:
                return int(response[0]['_id'].replace('AUCTION#', ''))
            return None
        except Exception as e:
            raise e

    def update_auction(self, auction: Auction = None, auction_dict: Dict = None) -> Dict or None:
        try:
            if auction:
                auction_dict = auction.to_dict()
            response = self.__dynamodb.update_item(
                Key={'_id': 'AUCTION#' + auction_dict.get('auction_id'),
                     'create_at': auction_dict.get('create_at')},
                UpdateExpression='SET tittle = :tittle, description = :description, start_date = :start_date, '
                                 'end_date = :end_date, start_amount = :start_amount, current_amount = :current_amount,'
                                 'images = :images, status_auction = :status_auction',
                ExpressionAttributeValues={
                    ':tittle': auction_dict.get('tittle'),
                    ':description': auction_dict.get('description'),
                    ':start_date': auction_dict.get('start_date'),
                    ':end_date': auction_dict.get('end_date'),
                    ':start_amount': Decimal(str(auction_dict.get('start_amount'))),
                    ':current_amount': Decimal(str(auction_dict.get('current_amount'))),
                    ':images': auction_dict.get('images'),
                    ':status_auction': auction_dict.get('status_auction').value
                },
                ReturnValues='UPDATED_NEW'
            )
        except Exception as e:
            raise e

    def update_auction_current_amount(self, auction_id: str = None, current_amount: float = None) -> Dict or None:
        try:
            response = self.__dynamodb.update_item(
                Key={'_id': 'AUCTION#' + auction_id},
                UpdateExpression='SET current_amount = :current_amount',
                ExpressionAttributeValues={
                    ':current_amount': Decimal(str(current_amount))
                },
                ReturnValues='UPDATED_NEW'
            )
        except Exception as e:
            raise e

    def get_last_bid_id(self) -> Optional[int]:
        try:
            query = self.__dynamodb.query(
                KeyConditionExpression=Key('_id').begins_with('BID#'),
                ScanIndexForward=False,
                Limit=1
            )
            response = query.get('Items', None)
            if response:
                return int(response[0]['_id'].replace('BID#', ''))
            return None
        except Exception as e:
            raise e

    def get_bids_by_auction(self, auction_id: str, exclusive_start_key: Optional[str] = None,
                            limit: Optional[int] = None) -> List[Dict]:
        try:
            query = self.__dynamodb.query(
                IndexName='sort_amount-index',
                KeyConditionExpression=Key('_id').begins_with('BID#'),
                FilterExpression=Attr('auction_id').eq(auction_id),
                Limit=limit,
                ScanIndexForward=False,
                ExclusiveStartKey={'_id': 'BID#' + exclusive_start_key} if exclusive_start_key else None
            )
            response = query.get('Items', None)
            if len(response) > 0:
                for bid in response:
                    bid['bid_id'] = bid.pop('_id').replace('BID#', '')
                    bid['amount'] = round(float(bid['amount']), 2)
            return response if len(response) > 0 else None
        except Exception as e:
            raise e

    def create_bid(self, bid: Bid) -> Dict or None:
        pass
