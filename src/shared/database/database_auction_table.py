from src.shared.database.database import Database


class AuctionDynamodb:
    def __int__(self):
        self.__dynamodb = Database().get_table_auction()

    def create_auction(self, auction: Auction) -> Dict or None:
        try:
            auction = auction.to_dict()
            self.__dynamodb.put_item(Item=auction)
            return {
                'body': auction
            }
        except Exception as e:
            raise e

    def create_bid(self, bid):
        try:
            bid = bid.to_dict()
            self.__dynamodb.put_item(Item=bid)
            return {
                'body': bid
            }
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
