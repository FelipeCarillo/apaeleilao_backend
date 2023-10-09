import os
from typing import Dict
from cryptography.fernet import Fernet

from .database import Database

from src.shared.structure.entities.user import User
from src.shared.structure.interface.user_interface import UserInterface


class UserDynamodb(UserInterface):

    def __init__(self):
        self.__dynamodb = Database().get_table_user()

    def create_user(self, user: User) -> Dict or None:
        try:
            user = user.to_dict()
            user['status_account'] = user['status_account'].value
            self.__dynamodb.put_item(Item=user)
            return {
                'body': user
            }
        except Exception as e:
            raise e

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

    def get_all_users(self, exclusive_start_key: str = None, limit: int = None) -> Dict or None:
        try:
            query = self.__dynamodb.scan(
                ExclusiveStartKey=exclusive_start_key,
                Limit=limit
            )
            response = query.get('Items', None)
            return response
        except Exception as e:
            raise e

    def get_user_by_email(self, email) -> Dict or None:
        try:
            query = self.__dynamodb.get_item(Key={'email': email})
            response = query.get('Item', None)
            return response
        except Exception as e:
            raise e

    def get_user_by_cpf(self, cpf) -> Dict or None:
        try:
            query = self.__dynamodb.scan(
                FilterExpression='cpf = :cpf',
                ExpressionAttributeValues={':cpf': cpf}
            )
            response = query.get('Items', None)
            return response[0] if response else None
        except Exception as e:
            raise e

    def update_user(self, email_auth: str, **kwargs) -> Dict or None:

        update_expression = 'SET '
        expression_attribute_values = {}

        for key, value in kwargs.items():
            if value is not None and value != 'email_auth':
                update_expression += f'{key} = :{key}, '
                expression_attribute_values[f':{key}'] = value

        update_expression = update_expression.rstrip(', ')

        try:
            query = self.__dynamodb.update_item(
                Key={'email': email_auth},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues='ALL_NEW'
            )
            return query.get('Attributes', None)
        except Exception as e:
            raise e
