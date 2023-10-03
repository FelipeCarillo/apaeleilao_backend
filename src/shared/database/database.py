import boto3


class Database:
    def __init__(self):
        self.__database_connection = boto3.resource('dynamodb')

    def get_table_user(self):
        return self.__database_connection.Table('UserApaeLeilao')

    def get_table_auction(self):
        return self.__database_connection.Table('AuctionApaeLeilao')