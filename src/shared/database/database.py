import os
import boto3


class Database:
    def __init__(self):
        self.__database_connection = boto3.resource('dynamodb')
        self.__user_table = os.environ.get('USER_TABLE')
        self.__auction_table = os.environ.get('AUCTION_TABLE')

    def get_table_user(self):
        return self.__database_connection.Table(self.__user_table)

    def get_table_auction(self):
        return self.__database_connection.Table(self.__auction_table)