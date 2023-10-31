import os
import boto3

if os.environ.get('STAGE') == 'test':
    resource = boto3.resource('dynamodb',
                              endpoint_url='http://localhost:8000',
                              region_name='dummy',
                              aws_access_key_id='dummy',
                              aws_secret_access_key='dummy'
                              )
else:
    resource = boto3.resource('dynamodb')


class Database:
    def __init__(self):
        self.__database_connection = resource
        self.__user_table = os.environ.get('USER_TABLE')
        self.__auction_table = os.environ.get('AUCTION_TABLE')

    def get_table_user(self):
        return self.__database_connection.Table(self.__user_table)

    def get_table_auction(self):
        return self.__database_connection.Table(self.__auction_table)
