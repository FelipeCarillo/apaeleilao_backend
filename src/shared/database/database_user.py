from typing import Dict, List, Optional
from boto3.dynamodb.conditions import Key

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
            user['PK'] = user.pop('user_id')
            user['SK'] = USER_TABLE_ENTITY.USER.value

            self.__dynamodb.put_item(
                Item=user
            )

            user['user_id'] = user.pop('PK')
            user.pop('SK')

            return user
        except Exception as e:
            raise e

    def authenticate(self,
                     access_key: str = None,
                     email: str = None,
                     ) -> Dict or None:
        try:
            if access_key:
                query = self.__dynamodb.query(
                    IndexName='access_key-index',
                    KeyConditionExpression=Key('access_key').eq(access_key),
                )
            else:
                query = self.__dynamodb.query(
                    IndexName='email-index',
                    KeyConditionExpression=Key('email').eq(email),
                )
            item = query.get('Items', None)
            item = item[0] if item else None
            if item:
                item['user_id'] = item.pop('PK')
                item.pop('SK')
                return item
            else:
                return None
        except Exception as e:
            raise e

    def get_user_by_id(self, user_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.query(
                KeyConditionExpression=Key('PK').eq(user_id) & Key('SK').eq(USER_TABLE_ENTITY.USER.value),
            ).get('Items', None)

            item = query[0] if query else None
            if item:
                item['user_id'] = item.pop('PK')
                item.pop('SK')
            return item
        except Exception as e:
            raise e

    def get_all_users(self, exclusive_start_key: str = None, limit: int = None,
                      type_account=None, status_account: str = None) -> Dict or None:
        try:
            if not exclusive_start_key:
                query = self.__dynamodb.query(
                    IndexName='SK-index',
                    KeyConditionExpression=Key('SK').eq(USER_TABLE_ENTITY.USER.value),
                    FilterExpression=Key('type_account').is_in(type_account) &
                                     Key('status_account').eq(status_account) if status_account else
                                     Key('type_account').is_in(type_account),
                    Limit=limit
                )
            else:
                query = self.__dynamodb.query(
                    IndexName='SK_type_account-index',
                    KeyConditionExpression=Key('SK').eq(USER_TABLE_ENTITY.USER.value) &
                                           Key('type_account').eq(type_account),

                    ExclusiveStartKey=exclusive_start_key,
                    Limit=limit
                )
            response = query.get('Items', None)
            if response:
                for item in response:
                    item['user_id'] = item.pop('PK')
                    item.pop('SK')
            return response
        except Exception as e:
            raise e

    def get_all_users_to_send_email(self) -> Optional[Dict]:
        try:
            query = self.__dynamodb.query(
                IndexName='SK_type_account-index',
                KeyConditionExpression=Key('SK').eq(USER_TABLE_ENTITY.USER.value) &
                                       Key('type_account').eq('USER'),
                FilterExpression=Key('status_account').eq('ACTIVE'),
                ProjectionExpression='email',
            )
            response = query.get('Items', None)
            if response:
                for item in response:
                    item['user_id'] = item.pop('PK')
                    item.pop('SK')
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
                response[0]['user_id'] = response[0].pop('PK')
                response[0].pop('SK')
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
                response[0]['user_id'] = response[0].pop('PK')
                response[0].pop('SK')
            return response[0] if response else None
        except Exception as e:
            raise e

    def get_user_by_access_key(self, access_key) -> Dict or None:
        try:
            query = self.__dynamodb.query(
                IndexName='access_key-index',
                KeyConditionExpression=Key('access_key').eq(access_key),
            )
            response = query.get('Items', None)
            if response:
                response[0]['user_id'] = response[0].pop('PK')
                response[0].pop('SK')
            return response[0] if response else None
        except Exception as e:
            raise e

    def update_user(self, user: User) -> Dict or None:
        try:
            response = self.__dynamodb.update_item(
                Key={
                    'PK': user.user_id,
                    'SK': USER_TABLE_ENTITY.USER.value
                },
                UpdateExpression='SET first_name = :first_name,'
                                 'last_name = :last_name,'
                                 'cpf = :cpf,'
                                 'phone = :phone,'
                                 'password = :password,'
                                 'accepted_terms = :accepted_terms,'
                                 'status_account = :status_account,'
                                 'type_account = :type_account,'
                                 'created_at = :created_at,'
                                 'verification_email_code = :verification_email_code,'
                                 'verification_email_code_expires_at = :verification_email_code_expires_at',
                ExpressionAttributeValues={
                    ':first_name': user.first_name,
                    ':last_name': user.last_name,
                    ':cpf': user.cpf,
                    ':phone': user.phone,
                    ':password': user.password,
                    ':accepted_terms': user.accepted_terms,
                    ':status_account': user.status_account.value,
                    ':type_account': user.type_account.value,
                    ':created_at': user.created_at,
                    ':verification_email_code': user.verification_email_code,
                    ':verification_email_code_expires_at': user.verification_email_code_expires_at,
                },
                ReturnValues='UPDATED_NEW'
            )['Attributes']
            if response:
                response.pop('SK')
                response['user_id'] = response.pop('PK')
                response['created_at'] = int(response['created_at'])
            return response if response else None
        except Exception as e:
            raise e

    def create_suspension(self, suspension) -> Dict or None:
        try:
            suspension = suspension.to_dict()
            suspension['PK'] = suspension.pop('user_id')
            suspension['SK'] = USER_TABLE_ENTITY.SUSPENSION.value + "#" + suspension.pop('suspension_id')

            self.__dynamodb.put_item(
                Item=suspension
            )

            suspension['user_id'] = suspension.pop('PK')
            suspension['suspension_id'] = suspension.pop('SK').split('#')[1]

            return suspension
        except Exception as e:
            raise e
