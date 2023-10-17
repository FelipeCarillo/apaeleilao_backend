import time
from typing import Dict

from src.shared.structure.entities.user import User
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM
from src.shared.helper_functions.time_manipulation import TimeManipulation
from src.shared.errors.modules_errors import MissingParameter, UserNotAuthenticated, InvalidParameter


class ConfirmVerificationEmailCodeUseCase:

    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface
        self.__token = TokenAuthy()

    def __call__(self, auth: Dict, body: Dict):
        if not auth:
            MissingParameter('auth')
        if not auth.get('Authorization'):
            MissingParameter('Authorization')

        if not body:
            MissingParameter('body')
        if not body.get('verification_email_code') and not body.get('password_reset_code'):
            raise MissingParameter('Código de validação')
        if body.get('verification_email_code') and body.get('password_reset_code'):
            raise InvalidParameter('verification_email_code ou password_reset_code',
                                   'não pode ser enviado os dois códigos ao mesmo tempo')

        decoded_token = self.__token.decode_token(auth['Authorization'])
        if not decoded_token:
            raise UserNotAuthenticated("Token de acesso inválido ou expirado.")
        user_id = decoded_token.get('user_id')
        user = self.__user_interface.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotAuthenticated()

        current_time = TimeManipulation().get_current_time()

        user_expire_at = user.get('password_reset_code_expires_at') if body.get('password_reset_code') else user.get(
            'verification_email_code_expires_at')
        user_code = user.get('password_reset_code') if body.get('password_reset_code') else user.get(
            'verification_email_code')
        request_code = body.get('password_reset_code') if body.get('password_reset_code') else body.get(
            'verification_email_code')

        if current_time > user_expire_at:
            raise InvalidParameter(parameter='Código de verificação', body='expirado')

        if int(request_code) != user_code:
            raise InvalidParameter(parameter='Código de verificação', body='inválido')

        status_account = STATUS_USER_ACCOUNT_ENUM.ACTIVE.value

        user = User(
            user_id=user.get('user_id'),
            first_name=user.get('first_name'),
            last_name=user.get('last_name'),
            cpf=user.get('cpf'),
            email=user.get('email'),
            phone=user.get('phone'),
            password=user.get('password'),
            accepted_terms=user.get('accepted_terms'),
            status_account=status_account,
            type_account=user.get('type_account'),
            date_joined=int(user.get('date_joined')),
            verification_email_code=None if body.get('verification_email_code') else user.get(
                'verification_email_code'),
            verification_email_code_expires_at=None if body.get('verification_email_code') else user.get(
                'verification_email_code_expires_at'),
            password_reset_code=None if body.get('password_reset_code') else user.get('password_reset_code'),
            password_reset_code_expires_at=None if body.get('password_reset_code') else user.get(
                'password_reset_code_expires_at')
        )

        return self.__user_interface.update_user(user)
