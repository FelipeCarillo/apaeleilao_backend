import boto3
import os

def create_tables():
    db = boto3.resource('dynamodb',
                        endpoint_url='http://localhost:8000',
                        region_name='dummy',
                        aws_access_key_id='dummy',
                        aws_secret_access_key='dummy')

    print('Creating user table...')
    user = db.create_table(
        TableName='User_Apae_Leilao',
        AttributeDefinitions=[
            {
                'AttributeName': 'PK',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'SK',
                'AttributeType': 'S'
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'PK',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'SK',
                'KeyType': 'RANGE'
            },
        ],
        BillingMode='PAY_PER_REQUEST',
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        },
    )

    print(f'User table created: {user}')
    print('|=====     | 50%')

    print('Creating auction table...')
    auction = db.create_table(
        TableName='Auction_Apae_Leilao',
        AttributeDefinitions=[
            {
                'AttributeName': 'PK',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'SK',
                'AttributeType': 'S'
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'PK',
                'KeyType': 'HASH',
            },
            {
                'AttributeName': 'SK',
                'KeyType': 'RANGE',
            },
        ],
        BillingMode='PAY_PER_REQUEST',
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        },
    )

    print(f'Auction table created: {auction}')
    print('|==========| 100%')
    print('Tables created successfully!')

    return user, auction


def create_GSIs(user, auction):
    user = user
    auction = auction
    pass


if __name__ == '__main__':
    user, auction = create_tables()
    create_GSIs(user, auction)
