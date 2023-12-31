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

    def get_all_auctions_admin(self, auctions_closed: bool = False) -> List[Optional[Dict]]:
        try:
            if not auctions_closed:
                permission_to_search = [STATUS_AUCTION_ENUM.OPEN.value, STATUS_AUCTION_ENUM.PENDING.value]
                query = self.__dynamodb.query(
                    IndexName="SK_start_date-index",
                    KeyConditionExpression=Key('SK').eq(AUCTION_TABLE_ENTITY.AUCTION.value),
                    FilterExpression=Attr('status_auction').eq(permission_to_search[0]) | Attr('status_auction').eq(
                        permission_to_search[1]),
                    ScanIndexForward=True,
                )
                response = query.get('Items', None)
                if response:
                    for auction in response:
                        auction.pop('SK')
                        auction['auction_id'] = auction.pop('PK')
                        auction['created_at'] = int(auction['created_at'])
                        auction['start_date'] = int(auction['start_date'])
                        auction['end_date'] = int(auction['end_date'])
                        auction['start_amount'] = round(float(auction['start_amount']), 2)
                        auction['current_amount'] = round(float(auction['current_amount']), 2)
                        if auction.get('status_auction') == STATUS_AUCTION_ENUM.OPEN.value:
                            bids = self.get_all_bids_by_auction_id(auction_id=auction.get('auction_id'))
                            auction['bids'] = bids
            else:
                permission_to_search = [STATUS_AUCTION_ENUM.CLOSED.value, STATUS_AUCTION_ENUM.AVAILABLE.value]
                query = self.__dynamodb.query(
                    IndexName="SK_start_date-index",
                    KeyConditionExpression=Key('SK').eq(AUCTION_TABLE_ENTITY.AUCTION.value),
                    FilterExpression=Attr('status_auction').eq(permission_to_search[0]) | Attr('status_auction').eq(
                        permission_to_search[1]),
                    ScanIndexForward=True,
                )
                response = query.get('Items', None)
                if response:
                    for auction in response:
                        auction.pop('SK')
                        auction['auction_id'] = auction.pop('PK')
                        auction['created_at'] = int(auction['created_at'])
                        auction['start_date'] = int(auction['start_date'])
                        auction['end_date'] = int(auction['end_date'])
                        auction['start_amount'] = round(float(auction['start_amount']), 2)
                        auction['current_amount'] = round(float(auction['current_amount']), 2)
                        if auction.get('status_auction') == STATUS_AUCTION_ENUM.CLOSED.value:
                            bids = self.get_all_bids_by_auction_id(auction_id=auction.get('auction_id'))
                            auction['bids'] = bids
                            payment = self.get_payment_by_auction(auction_id=auction.get('auction_id'))
                            auction['payment'] = payment
            return response if response else []
        except ClientError as e:
            raise e

    def get_all_auctions_menu(self) -> Optional[List[Dict]]:
        try:
            permission_to_search = [STATUS_AUCTION_ENUM.OPEN.value, STATUS_AUCTION_ENUM.PENDING.value]
            query = self.__dynamodb.query(
                IndexName="SK_start_date-index",
                KeyConditionExpression=Key('SK').eq(AUCTION_TABLE_ENTITY.AUCTION.value),
                FilterExpression=Attr('status_auction').eq(permission_to_search[0]) | Attr('status_auction').eq(
                    permission_to_search[1]),
                ScanIndexForward=True,
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
            permission_to_search = [STATUS_AUCTION_ENUM.OPEN.value, STATUS_AUCTION_ENUM.PENDING.value]
            query = self.__dynamodb.query(
                IndexName="SK_created_at-index",
                KeyConditionExpression=Key('SK').eq(AUCTION_TABLE_ENTITY.AUCTION.value),
                FilterExpression=Attr('start_date').between(start_date, end_date) | Attr('end_date').between(start_date, end_date),
                ScanIndexForward=False,
            )

            response = query.get('Items', None)
            if response:
                for auction in response:
                    if auction.get('status_auction') not in permission_to_search:
                        response.remove(auction)
                        continue
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
                IndexName="SK-index",
                KeyConditionExpression=Key('SK').eq(AUCTION_TABLE_ENTITY.AUCTION.value),
            )
            response = query.get('Items', None)
            if response:
                return int(sorted(response, key=lambda k: int(k['PK']), reverse=True)[0]['PK'])
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
                UpdateExpression='SET title = :title, description = :description, start_date = :start_date, '
                                 'end_date = :end_date, start_amount = :start_amount, current_amount = :current_amount,'
                                 'images = :images, status_auction = :status_auction',
                ExpressionAttributeValues={
                    ':title': auction_dict.get('title'),
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
                    ':current_amount': Decimal(str(round(current_amount, 2)))
                },
                ReturnValues='UPDATED_NEW'
            )
        except ClientError as e:
            raise e

    def get_last_bid_id(self, auction_id: str) -> Optional[int]:
        try:
            query = self.__dynamodb.query(
                KeyConditionExpression=Key('PK').eq(auction_id) & Key('SK').begins_with(AUCTION_TABLE_ENTITY.BID.value),
                ScanIndexForward=False,
                Limit=1
            )
            response = query.get('Items', None)
            if response:
                return int(response[0]['SK'].split('#')[-1])
            return None
        except ClientError as e:
            raise e

    def get_all_bids_by_auction_id(self, auction_id: str) -> List[Dict]:
        try:
            query = self.__dynamodb.query(
                KeyConditionExpression=Key('PK').eq(auction_id) & Key('SK').begins_with(AUCTION_TABLE_ENTITY.BID.value),
            )
            response = query.get('Items', [])
            if response:
                for bid in response:
                    bid['bid_id'] = bid.pop('SK').split('#')[1]
                    bid['auction_id'] = bid.pop('PK')
                    bid['amount'] = round(float(bid['amount']), 2)
                    bid['created_at'] = int(bid['created_at'])
                response = sorted(response, key=lambda k: k['amount'], reverse=True)
            return response
        except ClientError as e:
            raise e

    def create_bid(self, bid: Bid) -> Dict or None:
        try:
            payload = {
                "PK": bid.auction_id,
                "SK": AUCTION_TABLE_ENTITY.BID.value + "#" + bid.bid_id,
                "user_id": bid.user_id,
                "email": bid.email,
                "first_name": bid.first_name,
                "amount": Decimal(str(bid.amount)),
                "created_at": bid.created_at,
            }
            self.__dynamodb.put_item(Item=payload)

            return payload
        except ClientError as e:
            raise e

    def create_payment(self, payment) -> Dict or None:
        try:
            payload = {
                "PK": payment.auction_id,
                "SK": AUCTION_TABLE_ENTITY.PAYMENT.value + "#" + payment.payment_id,
                "user_id": payment.user_id,
                "status_payment": payment.status_payment.value,
                "amount": Decimal(str(payment.amount)),
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

    def get_all_auctions_user(self, user_id: str, status_auction: str = None) -> List[Optional[Dict]]:
        try:
            FilterExpression = Attr('SK').begins_with("PAYMENT") & Attr('status_auction').eq(status_auction) if status_auction else Attr('SK').begins_with("PAYMENT")

            payments = self.__dynamodb.query(
                IndexName="user_id-index",
                KeyConditionExpression=Key('user_id').eq(user_id),
                FilterExpression=FilterExpression,
            ).get('Items', None)
            if not payments:
                return []
            auctions_id = [auction.get("PK") for auction in payments]
            auctions = [
                self.__dynamodb.query(
                    KeyConditionExpression=Key('PK').eq(auction_id) & Key('SK').begins_with("AUCTION"),
                    FilterExpression=Attr('status_auction').eq(
                        "CLOSED")
                    ).get('Items')[0]
                for auction_id in auctions_id]
            merged_list = [{**auction, **payment} for auction, payment in zip(auctions, payments)]
            for auction in merged_list:
                auction['auction_id'] = auction.pop('PK')
                auction['payment_id'] = auction.pop('SK').split('#')[1]
                auction['amount'] = round(float(auction['amount']), 2)
                auction['end_date'] = int(auction['end_date'])
                auction['start_date'] = int(auction['start_date'])
                auction['start_amount'] = round(float(auction['start_amount']), 2)
                auction['current_amount'] = round(float(auction['current_amount']), 2)
                auction.pop("created_by")
                auction['created_at'] = int(auction['created_at'])
                auction['date_payment'] = int(auction['date_payment']) if auction['date_payment'] else None
                auction['payment_expires_at'] = int(auction['payment_expires_at'])
            return merged_list
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

    def get_payment_by_auction(self, auction_id: str) -> Optional[Dict]:
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
                response['amount'] = round(float(response['amount']), 2)
                response['date_payment'] = int(response['date_payment']) if response['date_payment'] else None
                response['payment_expires_at'] = int(response['payment_expires_at'])
                response['created_at'] = int(response['created_at'])
            return response
        except ClientError as e:
            raise e

    def update_status_payment(self, auction_id: str = None, payment_id: str = None, status_payment: str = None) -> \
            Optional[Dict]:
        try:
            response = self.__dynamodb.update_item(
                Key={'PK': auction_id,
                     'SK': AUCTION_TABLE_ENTITY.PAYMENT.value + "#" + payment_id},
                UpdateExpression='SET status_payment = :status_payment',
                ExpressionAttributeValues={
                    ':status_payment': status_payment
                },
                ReturnValues='ALL_NEW'
            )
            response['Attributes']['payment_id'] = response['Attributes'].pop('SK').split('#')[-1]
            response['Attributes']['auction_id'] = response['Attributes'].pop('PK')
            return response['Attributes']
        except ClientError as e:
            raise e
