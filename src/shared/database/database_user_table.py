from .database import Database
from typing import Any, Dict
from src.shared.structure.entities.user import User
from src.shared.structure.interface.user_interface import UserInterface


class UserDynamodb(UserInterface):

    def __init__(self):
        self.__dynamodb = Database().get_table_user()

    def create_user(self, user: User):
        try:
            self.__dynamodb.put_item(Item=user.to_dict())
            return {
                'body': user.to_dict()
            }
        except Exception as e:
            raise e

    def authenticate(self, user_id, password):
        try:
            response = self.__dynamodb.get_item(
                Key={
                    'user_id': user_id,
                    'password': password
                }
            )
            return response.get('Item', None)
        except Exception as e:
            raise e

    def get_all_users(self, exclusive_start_key: Any = None, limit: int = None):
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

    def get_user_by_email(self, email) -> User or None:
        try:
            response = self.__dynamodb.scan(
                FilterExpression='email = :email',
                ExpressionAttributeValues={
                    ':email': email
                }
            )
            return response.get('Items', None)
        except Exception as e:
            raise e

    def get_user_by_cpf(self, cpf) -> User or None:
        try:
            response = self.__dynamodb.scan(
                FilterExpression='cpf = :cpf',
                ExpressionAttributeValues={
                    ':cpf': cpf
                }
            )
            return response.get('Items', None)
        except Exception as e:
            raise e

    def update_user(self, user: User):
        pass
