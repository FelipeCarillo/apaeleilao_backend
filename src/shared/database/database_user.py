from typing import Dict, Optional
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from src.shared.database.database import Database
from src.shared.structure.entities.feedback import Feedback
from src.shared.structure.entities.user import User, UserModerator
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.table_entities import USER_TABLE_ENTITY
from src.shared.structure.enums.user_enum import TYPE_ACCOUNT_USER_ENUM
from src.shared.structure.enums.suspension_enum import STATUS_SUSPENSION_ENUM


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
        except ClientError as e:
            raise e

    def create_feedback(self, feedback: Feedback) -> Dict:
        try:
            feedback = feedback.to_dict()
            feedback['PK'] = feedback.pop('feedback_id')
            feedback['SK'] = USER_TABLE_ENTITY.FEEDBACK.value

            self.__dynamodb.put_item(
                Item=feedback
            )

            feedback['email'] = feedback.pop('SK')

            return feedback
        except ClientError as e:
            raise e

    def get_last_feedback_id(self) -> int:
        try:
            query = self.__dynamodb.query(
                IndexName='SK_created_at-index',
                KeyConditionExpression=Key('SK').eq(USER_TABLE_ENTITY.FEEDBACK.value),
                Limit=1
            )
            response = query.get('Items', None)
            if response:
                return int(response[0].get('PK'))
            else:
                return 0
        except ClientError as e:
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
        except ClientError as e:
            raise e

    def get_user_by_id(self, user_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.query(
                KeyConditionExpression=Key('PK').eq(user_id) & Key('SK').eq(USER_TABLE_ENTITY.USER.value),
            ).get('Items', [])
            item = None
            if len(query) > 0:
                item = query[0]
                item['user_id'] = item.pop('PK')
                item.pop('SK')
            return item
        except ClientError as e:
            raise e

    def get_all_users(self, type_account: TYPE_ACCOUNT_USER_ENUM = None) -> Dict or None:
        try:
            if type_account == "ADMIN":
                return None
            query = self.__dynamodb.query(
                IndexName='SK_type_account-index',
                KeyConditionExpression=Key('SK').eq(USER_TABLE_ENTITY.USER.value),
            ) if not type_account else self.__dynamodb.query(
                IndexName='SK_type_account-index',
                KeyConditionExpression=Key('SK').eq(USER_TABLE_ENTITY.USER.value) & Key('type_account').eq(type_account.value),
            )
            response = query.get('Items', [])
            if len(response) > 0:
                for user in response:
                    if user.get('type_account') == TYPE_ACCOUNT_USER_ENUM.ADMIN.value:
                        response.remove(user)
                        continue
                    user['user_id'] = user.pop('PK')
                    user.pop('SK')
                    user['created_at'] = int(user['created_at']) if user.get("created_at") else None
                    user['verification_email_code_expires_at'] = int(user['verification_email_code_expires_at']) if user.get("verification_email_code_expires_at") else None
                    suspensions = self.get_all_suspensions_by_user_id(user['user_id'])
                    user['suspensions'] = suspensions if suspensions else None
            return response if response else None

        except ClientError as e:
            raise e

    def get_all_users_to_send_email(self) -> Optional[Dict]:
        try:
            query = self.__dynamodb.query(
                IndexName='SK_type_account-index',
                KeyConditionExpression=Key('SK').eq(USER_TABLE_ENTITY.USER.value) & Key('type_account').eq('USER'),
                FilterExpression=Key('status_account').eq('ACTIVE'),
                ProjectionExpression='email',
            )
            response = query.get('Items', None)
            if response:
                response = [email['email'] for email in response]
            return response
        except ClientError as e:
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
        except ClientError as e:
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
        except ClientError as e:
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
        except ClientError as e:
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
                ReturnValues='ALL_NEW'
            )['Attributes']
            if response:
                response.pop('SK')
                response['user_id'] = response.pop('PK')
                response['created_at'] = int(response['created_at'])
            return response if response else None
        except ClientError as e:
            raise e

    def update_user_status(self, user_id: str, status: str) -> Dict or None:
        try:
            response = self.__dynamodb.update_item(
                Key={
                    'PK': user_id,
                    'SK': USER_TABLE_ENTITY.USER.value
                },
                UpdateExpression='SET status_account = :status_account',
                ExpressionAttributeValues={
                    ':status_account': status,
                },
                ReturnValues='ALL_NEW'
            )['Attributes']
            if response:
                response.pop('SK')
                response['user_id'] = response.pop('PK')
                response['created_at'] = int(response['created_at'])
            return response if response else None
        except ClientError as e:
            raise e

    def get_all_suspensions_by_user_id(self, user_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.query(
                KeyConditionExpression=Key('PK').eq(user_id) & Key('SK').begins_with(USER_TABLE_ENTITY.SUSPENSION.value)
            )
            response = query.get('Items', [])
            if len(response) > 0:
                for item in response:
                    item['user_id'] = item.pop('PK')
                    item['created_at'] = int(item['created_at']) if item.get('created_at') else None
                    item['date_suspension'] = int(item['date_suspension']) if item.get('date_suspension') else None
                    item['date_reactivation'] = int(item['date_reactivation']) if item.get('date_reactivation') else None
                    item['suspension_id'] = item.pop('SK').split('#')[1]
            return response if response else None
        except ClientError as e:
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
        except ClientError as e:
            raise e

    def update_suspension_status(self, user_id: str, status: STATUS_SUSPENSION_ENUM) -> Dict or None:
        try:
            response = self.__dynamodb.update_item(
                Key={
                    'PK': user_id,
                    'SK': USER_TABLE_ENTITY.SUSPENSION.value
                },
                UpdateExpression='SET status_suspension = :status_suspension',
                ExpressionAttributeValues={
                    ':status_suspension': status.value,
                },
                ReturnValues='ALL_NEW'
            )['Attributes']
            if response:
                response.pop('SK')
                response['user_id'] = response.pop('PK')
                response['created_at'] = int(response['created_at'])
            return response if response else None
        except ClientError as e:
            raise e

    def get_all_feedbacks(self) -> Dict or None:
        try:
            query = self.__dynamodb.query(
                IndexName='SK_created_at-index',
                KeyConditionExpression=Key('SK').eq(USER_TABLE_ENTITY.FEEDBACK.value),
            )
            response = query.get('Items', None)
            if response:
                for item in response:
                    item['email'] = item.pop('SK')
                    item['feedback_id'] = item.pop('PK')
                    item['created_at'] = int(item['created_at'])
                    item['grade'] = int(item['grade'])
            return response if response else None
        except ClientError as e:
            raise e

    def get_suspension_by_id(self, suspension_id: str) -> Dict or None:
        try:
            query = self.__dynamodb.query(
                IndexName="SK_created_at-index",
                KeyConditionExpression=Key('SK').eq(USER_TABLE_ENTITY.SUSPENSION.value + "#" + suspension_id),
            )
            response = query.get('Items', None)
            if response:
                response[0]['user_id'] = response[0].pop('PK')
                response[0]['suspension_id'] = response[0].pop('SK').split('#')[1]
                response[0]['created_at'] = int(response[0]['created_at']) if response[0].get('created_at') else None
                response[0]['date_suspension'] = int(response[0]['date_suspension'])
                response[0]['date_reactivation'] = int(response[0]['date_reactivation']) if response[0].get('date_reactivation') else None
            return response[0] if response else None
        except ClientError as e:
            raise e
