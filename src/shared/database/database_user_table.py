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
            self.__dynamodb.put_item(Item=user)
            return {
                'body': user
            }
        except Exception as e:
            raise e

    def authenticate(self, email: str, password: str = None, password_hash: str = None) -> Dict or None:

        encrypted_key = os.environ.get('ENCRYPTED_KEY').encode('utf-8')
        f = Fernet(encrypted_key)

        try:
            Key = {"email": email}
            query = self.__dynamodb.get_item(Key=Key)
            item = query.get('Item', None)

            if not item:
                return None

            real_password = f.decrypt(item.get('password').encode('utf-8')).decode('utf-8')

            if password_hash:
                password_hash = f.decrypt(password_hash.encode('utf-8')).decode('utf-8')
                return item if real_password == password_hash else None
            if password:
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

    def update_user(self, user: User) -> Dict or None:
        try:
            user = user
            response = self.__dynamodb.update_item(
                Key={'email': user.email},
                UpdateExpression='SET first_name = :first_name,'
                                 'last_name = :last_name,'
                                 'cpf = :cpf,'
                                 'phone = :phone,'
                                 'password = :password,'
                                 'accepted_terms = :accepted_terms,'
                                 'status_account = :status_account,'
                                 'suspensions = :suspensions,'
                                 'type_account = :type_account,'
                                 'verification_email_code = :verification_email_code, '
                                 'verification_email_code_expires_at = :verification_email_code_expires_at, '
                                 'password_reset_code = :password_reset_code, '
                                 'password_reset_code_expires_at = :password_reset_code_expires_at',
                ExpressionAttributeValues={
                    ':first_name': user.first_name,
                    ':last_name': user.last_name,
                    ':cpf': user.cpf,
                    ':phone': user.phone,
                    ':password': user.password,
                    ':accepted_terms': user.accepted_terms,
                    ':status_account': user.status_account,
                    ':suspensions': user.suspensions,
                    ':type_account': user.type_account,
                    ':verification_email_code': user.verification_email_code,
                    ':verification_email_code_expires_at': user.verification_email_code_expires_at,
                    ':password_reset_code': user.password_reset_code,
                    ':password_reset_code_expires_at': user.password_reset_code_expires_at
                },
                ReturnValues='UPDATED_NEW'
            )
            return response['Attributes'] if response else None
        except Exception as e:
            raise e
