from typing import Dict

from bcrypt import checkpw
from boto3.dynamodb.conditions import Key, Attr

from src.shared.database.database import Database
from src.shared.structure.entities.user import User, UserModerator
from src.shared.structure.enums.table_entities import USER_TABLE_ENTITY
from src.shared.structure.interface.user_interface import UserInterface


class UserDynamodb(UserInterface):

    def __init__(self):
        self.__dynamodb = Database().get_table_user()

    def create_user(self, user: User or UserModerator) -> Dict or None:
        try:
            user = user.to_dict()
            user['_id'] = USER_TABLE_ENTITY.USER.value+"#"+user.pop('user_id')

            self.__dynamodb.put_item(
                Item=user
            )
            return user
        except Exception as e:
            raise e

    def authenticate(self,
                     access_key: str = None,
                     email: str = None,
                     password: str = None,
                     ) -> Dict or None:
        try:
            if access_key:
                query = self.__dynamodb.query(IndexName='access_key-index',
                                              KeyConditionExpression=Key('access_key').eq(access_key))
            else:
                query = self.__dynamodb.query(IndexName='email-index',
                                              KeyConditionExpression=Key('email').eq(email))
            item = query.get('Items', None)
            item = item[0] if item else None
            if item:
                if checkpw(password.encode('utf-8'), item['password'].encode('utf-8')):
                    item['user_id'] = item.pop('_id').split('#')[-1]
                    return item
                else:
                    return None
            else:
                return None
        except Exception as e:
            raise e

    def get_user_by_id(self, user_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.query(KeyConditionExpression=Key('_id').eq(USER_TABLE_ENTITY.USER.value+"#"+user_id),
                                          FilterExpression=Key('create_at').gte(0)
                                          ).get('Items', None)
            item = query[0] if query else None
            if item:
                item['user_id'] = item.pop('_id').split('#')[-1]
            return item
        except Exception as e:
            raise e

    def get_all_users(self, exclusive_start_key: str = None, limit: int = None, type_account: str = 'USER') -> Dict or None:
        try:
            query = self.__dynamodb.scan(
                ExclusiveStartKey=exclusive_start_key,
                Limit=limit,
                FilterExpression=Attr('_id').begins_with('USER#')
            )
            response = query.get('Items', None)
            if response:
                for item in response:
                    item['user_id'] = item.pop('_id').split('#')[-1]
            return response
        except Exception as e:
            raise e

    def get_user_by_email(self, email) -> Dict or None:
        try:
            query = self.__dynamodb.query(
                IndexName='email-index',
                KeyConditionExpression=Key('email').eq(email),
            )
            response = query.get('Items', None)
            if response:
                response[0]['user_id'] = response[0].pop('_id').split('#')[-1]
            return response[0] if response else None
        except Exception as e:
            raise e

    def get_user_by_cpf(self, cpf) -> Dict or None:
        try:
            query = self.__dynamodb.query(
                IndexName='cpf-index',
                KeyConditionExpression=Key('cpf').eq(cpf),
            )
            response = query.get('Items', None)
            if response:
                response[0]['user_id'] = response[0].pop('_id').split('#')[-1]
            return response[0] if response else None
        except Exception as e:
            raise e

    def update_user(self, user: User) -> Dict or None:
        try:
            response = self.__dynamodb.update_item(
                Key={'_id': USER_TABLE_ENTITY.USER.value+"#"+user.user_id},
                UpdateExpression='SET first_name = :first_name,'
                                 'last_name = :last_name,'
                                 'cpf = :cpf,'
                                 'phone = :phone,'
                                 'password = :password,'
                                 'accepted_terms = :accepted_terms,'
                                 'status_account = :status_account,'
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
                    ':status_account': user.status_account.value,
                    ':type_account': user.type_account.value,
                    ':verification_email_code': user.verification_email_code,
                    ':verification_email_code_expires_at': user.verification_email_code_expires_at,
                    ':password_reset_code': user.password_reset_code,
                    ':password_reset_code_expires_at': user.password_reset_code_expires_at
                },
                ReturnValues='ALL_NEW'
            )
            if response:
                response['Attributes']['user_id'] = response['Attributes'].pop('_id').split('#')[-1]
            return response['Attributes'] if response else None
        except Exception as e:
            raise e
