import os
import time
import boto3
import random
from typing import Dict

from src.shared.structure.interface.user_interface import UserInterface
from src.shared.errors.modules_errors import MissingParameter, UserNotAuthenticated


class SendEmailCodeUseCase:
    ses_region = os.environ.get('SES_REGION')
    ses_sender = os.environ.get('SES_SENDER')

    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface
        self.__ses = boto3.client('ses', region_name=self.ses_region)

    def __call__(self, auth: Dict):
        if not auth:
            MissingParameter('auth')

        auth = self.__user_interface.authenticate(email=auth['email'], password=auth['password'])
        if not auth:
            raise UserNotAuthenticated()

        verification_email_code = random.randint(10000, 99999)
        verification_email_code_expires_at = time.time() + 3600

        self.__user_interface.update_user(email=auth['auth'],
                                          verification_email_code_expires_at=verification_email_code_expires_at,
                                          verification_email_code=verification_email_code)

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
