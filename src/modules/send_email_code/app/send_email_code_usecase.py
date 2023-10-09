import os
import time
import boto3
import random
from typing import Dict

from src.shared.structure.entities.user import User
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.errors.modules_errors import MissingParameter, UserNotAuthenticated
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM


class SendEmailCodeUseCase:
    ses_region = os.environ.get('SES_REGION')
    ses_sender = os.environ.get('SES_SENDER')

    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface
        self.__ses = boto3.client('ses', region_name=self.ses_region)

    def __call__(self, auth: Dict):
        if not auth:
            MissingParameter('auth')
        if not auth['email']:
            MissingParameter('email')
        if not auth['password']:
            MissingParameter('password')

        auth = self.__user_interface.authenticate(email=auth['email'], password=auth['password'])
        if not auth:
            raise UserNotAuthenticated()

        verification_email_code = random.randint(10000, 99999)
        verification_email_code_expires_at = int(time.time()) + 3600

        user = User(user_id=auth['user_id'], first_name=auth['first_name'], last_name=auth['last_name'],
                    cpf=auth['cpf'], email=auth['email'], phone=auth['phone'], password=auth['password'],
                    accepted_terms=auth['accepted_terms'], status_account=auth['status_account'],
                    suspensions=auth['suspensions'], date_joined=auth['date_joined'],
                    verification_email_code=verification_email_code,
                    verification_email_code_expires_at=verification_email_code_expires_at,
                    password_reset_code=auth['password_reset_code'],
                    password_reset_code_expires_at=auth['password_reset_code_expires_at'])

        self.__user_interface.update_user(user)

        email_format = f"""
        <html>
            <head></head>
            <body>
                <h1>Seu código de verificação é {verification_email_code}</h1>
            </body>
        </html>
        """

        self.__ses.meta.client.send_email(
            Destination={
                'ToAddresses': [
                    auth['email'],
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': email_format,
                    }
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': 'Código de verificação',
                }
            },
            Source=self.ses_sender,
        )

        return {'body': {'email': auth['email'],
                         'verification_email_code_expires_at': verification_email_code_expires_at}}
