import boto3


class Dynamodb:
    def __init__(self):
        self.__dynamo_connection = boto3.resource('dynamodb')

    def get_table_user(self):
        table = self.__dynamo_connection.Table('User_Apae_Leilao')
        return table

    def get_table_auction(self):
        table = self.__dynamo_connection.Table('Auction_Apae_Leilao')
        return table

