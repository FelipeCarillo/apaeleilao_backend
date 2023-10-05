import os
from typing import Any, Dict

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

    def authenticate(self, user_id: str = None, email: str = None, cpf: str = None,
                     password: str = None) -> Dict or None:
        response: Dict = {}
        try:
            if user_id:
                response = self.__dynamodb.get_item(
                    Key={
                        'user_id': {'S': user_id},
                        'password': {'S': password}
                    }
                )
                item = response.get('Item', None)
                return item

            if email:
                response = self.__dynamodb.scan(
                    FilterExpression='email = :email AND password = :password',
                    ExpressionAttributeValues={
                        ':email': {
                            'S': email
                        },
                        ':password': {
                            'S': password
                        }
                    }
                )

            item = response.get('Items', None)
            return item[0] if item else None
        except Exception as e:
            raise e

    def get_all_users(self, exclusive_start_key: str = None, limit: int = None) -> Dict or None:
        try:
            response = self.__dynamodb.scan(
                ExclusiveStartKey=exclusive_start_key,
                Limit=limit
            )
            return response.get('Items', None)
        except Exception as e:
            raise e

    def get_user_by_id(self, user_id) -> Dict or None:
        try:
            response = self.__dynamodb.get_item(
                Key={
                    'user_id': user_id
                }
            )
            return response.get('Item', None)
        except Exception as e:
            raise e

    def get_user_by_email(self, email) -> Dict or None:
        try:
            response = self.__dynamodb.scan(
                FilterExpression='email = :email',
                ExpressionAttributeValues={
                    ':email': {
                        'S': email
                    }
                }
            )
            return response.get('Items', None)
        except Exception as e:
            raise e

    def get_user_by_cpf(self, cpf) -> Dict or None:
        try:
            response = self.__dynamodb.scan(
                FilterExpression='cpf = :cpf',
                ExpressionAttributeValues={
                    ':cpf': {
                        'S': cpf
                    }
                }
            )
            return response.get('Items', None)
        except Exception as e:
            raise e

    def update_user(self, user: User):
        pass
