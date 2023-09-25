import boto3

class DockerDynamodb:
    def __init__(self):
        self.__dynamo_resource = boto3.resource('dynamodb',
                                                endpoint_url='http://localhost:8000',
                                                region_name='dummy')
        if 'User_Apae_Leilao' not in self.__dynamo_resource.meta.client.list_tables()['TableNames']:
            self.__dynamo_resource.create_table(
                TableName='User_Apae_Leilao',
                KeySchema=[
                    {
                        'AttributeName': 'user_id',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'user_id',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
        if 'Auction_Apae_Leilao' not in self.__dynamo_resource.meta.client.list_tables()['TableNames']:
            self.__dynamo_resource.create_table(
                TableName='Auction_Apae_Leilao',
                KeySchema=[
                    {
                        'AttributeName': 'auction_id',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'auction_id',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )

    def get_table_user(self):
        table = self.__dynamo_resource.Table('User_Apae_Leilao')
        return table

    def get_table_product(self):
        table = self.__dynamo_resource.Table('Auction_Apae_Leilao')
        return table
