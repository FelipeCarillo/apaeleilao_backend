from decimal import Decimal
from typing import Dict, List, Optional
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

from src.shared.database.database import Database
from src.shared.structure.entities.bid import Bid
from src.shared.structure.entities.auction import Auction
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM
from src.shared.structure.enums.table_entities import AUCTION_TABLE_ENTITY
from src.shared.structure.interface.auction_interface import AuctionInterface


class AuctionDynamodb(AuctionInterface):
    def __init__(self):
        self.__dynamodb = Database().get_table_auction()

    def create_auction(self, auction: Auction) -> Dict or None:
        try:
            auction = auction.to_dict()
            auction['PK'] = auction.pop('auction_id')
            auction['SK'] = AUCTION_TABLE_ENTITY.AUCTION.value
            auction['start_amount'] = Decimal(str(auction['start_amount']))
            auction['current_amount'] = Decimal(str(auction['current_amount']))
            self.__dynamodb.put_item(Item=auction)

            auction['auction_id'] = auction.pop('PK')
            auction.pop('SK')
            return auction
        except ClientError as e:
            raise e

    def get_all_auctions(self, exclusive_start_key: str = None, amount: int = 6, scan_forward: bool = False,
                         status_to_search: STATUS_AUCTION_ENUM = None) -> List[Dict] or None:
        pass

    #     try:
    #         exclusive_start_key = "AUCTION#" + exclusive_start_key if exclusive_start_key else None
    #         get_auction_expression = Key('_id').begins_with('AUCTION#')
    #         get_status_auction_expression = Attr('status_auction').eq(
    #             status_to_search.value) if status_to_search else None
    #         if get_status_auction_expression:
    #             get_auction_expression = get_auction_expression & get_status_auction_expression
    #
    #         if not exclusive_start_key:
    #             query = self.__dynamodb.query(
    #                 KeyConditionExpression=get_auction_expression,
    #                 Limit=amount,
    #                 ScanIndexForward=scan_forward
    #             )
    #         else:
    #             query = self.__dynamodb.query(
    #                 KeyConditionExpression=get_auction_expression,
    #                 Limit=amount,
    #                 ScanIndexForward=scan_forward,
    #                 ExclusiveStartKey={'_id': exclusive_start_key}
    #             )
    #         response = query.get('Items', None)
    #         if response:
    #             for auction in response:
    #                 auction['auction_id'] = auction.pop('_id').replace('AUCTION#', '')
    #                 auction['start_amount'] = round(float(auction['start_amount']), 2)
    #                 auction['current_amount'] = round(float(auction['current_amount']), 2)
    #         return response
    #     except ClientError as e:
    #         raise e

    def get_all_auctions_menu(self) -> Optional[List[Dict]]:
        try:
            permission_to_search = STATUS_AUCTION_ENUM.OPEN.value or STATUS_AUCTION_ENUM.PENDING.value
            query = self.__dynamodb.query(
                IndexName="SK_created_at-index",
                KeyConditionExpression=Key('SK').eq(AUCTION_TABLE_ENTITY.AUCTION.value),
                FilterExpression=Attr('status_auction').eq(permission_to_search),
                ScanIndexForward=False,
                Limit=6,
            )

            response = query.get('Items', None)
            if response:
                for auction in response:
                    auction.pop('SK')
                    auction['auction_id'] = auction.pop('PK')
                    auction['start_amount'] = round(float(auction['start_amount']), 2)
                    auction['current_amount'] = round(float(auction['current_amount']), 2)
            return response if len(response) > 0 else None
        except ClientError as e:
            raise e

    def get_auction_between_dates(self, start_date: int, end_date: int) -> List[Dict] or None:
        try:
            permission_to_search = STATUS_AUCTION_ENUM.OPEN.value or STATUS_AUCTION_ENUM.PENDING.value
            query = self.__dynamodb.query(
                IndexName="SK_created_at-index",
                KeyConditionExpression=Key('SK').eq(AUCTION_TABLE_ENTITY.AUCTION.value),
                FilterExpression=Attr('status_auction').eq(permission_to_search) &
                                 Attr('start_date').between(start_date, end_date),
                ScanIndexForward=False,
            )

            response = query.get('Items', None)
            if response:
                for auction in response:
                    auction.pop('SK')
                    auction['auction_id'] = auction.pop('PK')
                    auction['start_amount'] = round(float(auction['start_amount']), 2)
                    auction['current_amount'] = round(float(auction['current_amount']), 2)
            return response if len(response) > 0 else None
        except ClientError as e:
            raise e

    def get_auction_by_id(self, auction_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.get_item(
                Key={'PK': auction_id,
                     'SK': AUCTION_TABLE_ENTITY.AUCTION.value
                     }
            ).get('Item', None)

            item = query if query else None
            if item:
                item.pop('SK')
                item['auction_id'] = item.pop('PK')
                item['start_amount'] = round(float(item['start_amount']), 2)
                item['current_amount'] = round(float(item['current_amount']), 2)
            return item
        except ClientError as e:
            raise e

    def get_last_auction_id(self) -> int or None:
        try:
            query = self.__dynamodb.query(
                IndexName="SK_PK-index",
                KeyConditionExpression=Key('SK').eq(AUCTION_TABLE_ENTITY.AUCTION.value),
                ScanIndexForward=False,
                Limit=1
            )
            response = query.get('Items', None)
            if response:
                return int(response[0]['PK'])
            return None
        except ClientError as e:
            raise e

    def update_auction(self, auction: Auction = None, auction_dict: Dict = None) -> Dict or None:
        try:
            if auction:
                auction_dict = auction.to_dict()
            response = self.__dynamodb.update_item(
                Key={'PK': auction_dict.get('auction_id'),
                     'SK': AUCTION_TABLE_ENTITY.AUCTION.value},
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
                    ':status_auction': auction_dict.get('status_auction')
                },
                ReturnValues='ALL_NEW'
            )

            response['Attributes'].pop('SK')
            response['Attributes']['auction_id'] = response['Attributes'].pop('PK')
            response['Attributes']['start_amount'] = round(float(response['Attributes']['start_amount']), 2)
            response['Attributes']['current_amount'] = round(float(response['Attributes']['current_amount']), 2)
            return response['Attributes']
        except ClientError as e:
            raise e

    def update_auction_current_amount(self, auction_id: str = None, current_amount: float = None) -> Dict or None:
        try:
            response = self.__dynamodb.update_item(
                Key={'PK': auction_id,
                     'SK': AUCTION_TABLE_ENTITY.AUCTION.value},
                UpdateExpression='SET current_amount = :current_amount',
                ExpressionAttributeValues={
                    ':current_amount': Decimal(str(round(current_amount,2)))
                },
                ReturnValues='UPDATED_NEW'
            )
        except ClientError as e:
            raise e

    def get_last_bid_id(self) -> Optional[int]:
        try:
            query = self.__dynamodb.query(
                IndexName="SK_PK-index",
                KeyConditionExpression=Key('SK').eq(AUCTION_TABLE_ENTITY.BID.value),
                ScanIndexForward=False,
                Limit=1
            )
            response = query.get('Items', None)
            if response:
                return int(response[0]['SK'].split('#')[1])
            return None
        except ClientError as e:
            raise e

    def get_all_bids_by_auction_id(self, auction_id: str) -> List[Dict]:
        try:
            query = self.__dynamodb.query(
                KeyConditionExpression=Key('PK').eq(auction_id) & Key('SK').begins_with(AUCTION_TABLE_ENTITY.BID.value),
            )
            response = query.get('Items', None)
            if response:
                for bid in response:
                    bid['bid_id'] = bid.pop('SK').split('#')[1]
                    bid['auction_id'] = bid.pop('PK')
                    bid['amount'] = round(float(bid['amount']), 2)
            return response
        except ClientError as e:
            raise e

    def create_bid(self, bid: Bid) -> Dict or None:
        pass

    def create_payment(self, payment) -> Dict or None:
        try:
            payload = {
                "PK": payment.auction_id,
                "SK": AUCTION_TABLE_ENTITY.PAYMENT.value + "#" + payment.payment_id,
                "user_id": payment.user_id,
                "status_payment": payment.status_payment.value,
                "amount": payment.amount,
                "date_payment": payment.date_payment,
                "payment_expires_at": payment.payment_expires_at,
                "service": payment.payment_service.value,
                "created_at": payment.created_at,
            }
            self.__dynamodb.put_item(Item=payload)
            return payload
        except ClientError as e:
            raise e

    def get_payment_by_id(self, payment_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.query(
                IndexName="SK-index",
                KeyConditionExpression=Key('SK').eq(AUCTION_TABLE_ENTITY.PAYMENT.value + "#" + payment_id),
            )
            response = query.get('Items', None)
            if response:
                response = response[0]
                response['payment_id'] = response.pop('SK').split('#')[1]
                response['auction_id'] = response.pop('PK')
            return response
        except ClientError as e:
            raise e

    def get_payment_by_auction_id(self, auction_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.query(
                KeyConditionExpression=Key('PK').eq(auction_id) & Key('SK').begins_with(
                    AUCTION_TABLE_ENTITY.PAYMENT.value),
            )
            response = query.get('Items', None)
            if response:
                response = response[0]
                response['payment_id'] = response.pop('SK').split('#')[1]
                response['auction_id'] = response.pop('PK')
            return response
        except ClientError as e:
            raise e

    def get_payment_by_user_id(self, user_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.query(
                IndexName="user_id-index",
                KeyConditionExpression=Key('user_id').eq(user_id),
                FilterExpression=Attr('SK').begins_with(AUCTION_TABLE_ENTITY.PAYMENT.value),
            )
            response = query.get('Items', None)
            if response:
                response = response[0]
                response['payment_id'] = response.pop('SK').split('#')[1]
                response['auction_id'] = response.pop('PK')
            return response
        except ClientError as e:
            raise e
