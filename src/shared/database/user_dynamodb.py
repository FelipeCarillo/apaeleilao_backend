import os
import boto3
import uuid
from .dynamodb import Dynamodb
from src.shared.structure.entities.user import User


class UserDynamodb:
    def __init__(self):
        self.__dynamodb = Dynamodb().get_table_user()

    def authenticate(self, user_id, password):
        try:
            response = self.__dynamodb.get_item(
                Key={
                    'user_id': user_id,
                    'password': password
                }
            )
            if 'Item' in response:
                return response['Item']
            else:
                return None
        except Exception as e:
            raise e

    def get_user_by_id(self, user_id) -> User or None:
        try:
            response = self.__dynamodb.get_item(
                Key={
                    'user_id': user_id
                }
            )
            if 'Item' in response:
                return User(**response['Item'])
            else:
                return None
        except Exception as e:
            raise e

    def get_user_by_email(self, email) -> User or None:
        pass

    def get_user_by_cpf(self, cpf) -> User or None:
        pass

    def create_user(self, user: User):
        try:
            self.__dynamodb.put_item(
                Item=user.to_dict()
            )
        except Exception as e:
            raise e

    def update_user(self, user: User):
        pass

    def delete_user(self, user_id):
        pass
