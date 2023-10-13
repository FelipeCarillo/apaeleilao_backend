import os
import time
import boto3
from typing import Dict

from src.shared.structure.entities.user import User
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM
from src.shared.errors.modules_errors import MissingParameter, UserNotAuthenticated, InvalidParameter

class ConfirmEmailCodeUsecase:

    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface
        self.__client = boto3.client('ses', region_name=os.environ.get('SES_REGION'))

    def __call__(self, auth: Dict, body: Dict):
        if not auth:
            MissingParameter('auth')
        if not auth.get('email'):
            MissingParameter('email')
        if not auth.get('password'):
            MissingParameter('password')
        if not body:
            MissingParameter('body')
        if not body.get('verification_email_code'):
            MissingParameter('verification_email_code')

        auth = self.__user_interface.authenticate(user_id=auth['user_id'], password=auth['password'])
        if not auth:
            raise UserNotAuthenticated()

        current_time = int(time.time()) - 3 * 3600

        if current_time > auth.get('verification_email_code_expires_at'):
            raise InvalidParameter(parameter='Código de verificação', body='expirado')

        if int(body['verification_email_code']) != auth.get('verification_email_code'):
            raise InvalidParameter(parameter='Código de verificação', body='inválido')

        status_account = STATUS_USER_ACCOUNT_ENUM.ACTIVE.value

        user = User(
            user_id=auth.get('user_id'),
            first_name=auth.get('first_name'),
            last_name=auth.get('last_name'),
            cpf=auth.get('cpf'),
            email=auth.get('email'),
            phone=auth.get('phone'),
            password=auth.get('password'),
            accepted_terms=auth.get('accepted_terms'),
            status_account=status_account,
            type_account=auth.get('type_account'),
            suspensions=auth.get('suspensions'),
            date_joined=int(auth.get('date_joined')),
            verification_email_code=None,
            verification_email_code_expires_at=None,
            password_reset_code=auth.get('password_reset_code'),
            password_reset_code_expires_at=auth.get('password_reset_code_expires_at')
        )

        return self.__user_interface.update_user(user)
