import os
from typing import Dict
from cryptography.fernet import Fernet

from database import Database
from src.shared.structure.entities.auction import Auction
from src.shared.structure.interface.auction_interface import AuctionInterface


class AuctionDynamodb(AuctionInterface):
    def __init__(self):
        self.__dynamodb = Database().get_table_auction()
        self.__dynamodb_user = Database().get_table_user()

    def authenticate(self, email: str, password: str) -> Dict or None:

        encrypted_key = os.environ.get('ENCRYPTED_KEY').encode('utf-8')
        f = Fernet(encrypted_key)

        try:
            Key = {"email": email}
            query = self.__dynamodb.get_item(Key=Key)
            item = query.get('Item', None)

            if not item:
                return None

            real_password = f.decrypt(item.get('password').encode('utf-8')).decode('utf-8')

            return item if real_password == password else None
        except Exception as e:
            raise e

    def create_auction(self, auction: Auction) -> Dict or None:
        pass

    def get_all_auctions(self, exclusive_start_key: str = None, limit: int = None) -> Dict or None:
        pass



