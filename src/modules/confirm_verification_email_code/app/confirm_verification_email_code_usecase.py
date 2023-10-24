import time
from typing import Dict

from src.shared.structure.entities.user import User
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM, TYPE_ACCOUNT_USER_ENUM
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
        if not body.get('verification_email_code'):
            raise MissingParameter('Código de validação')

        decoded_token = self.__token.decode_token(auth['Authorization'])
        if not decoded_token:
            raise UserNotAuthenticated("Token de acesso inválido ou expirado.")
        user_id = decoded_token.get('user_id')
        user = self.__user_interface.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotAuthenticated()

        if user.get('status_account') != STATUS_USER_ACCOUNT_ENUM.PENDING.value:
            raise InvalidParameter(parameter='Conta', body='já verificada')

        if TYPE_ACCOUNT_USER_ENUM(user.get('type_account')) != TYPE_ACCOUNT_USER_ENUM.USER:
            raise UserNotAuthenticated(message='Você não tem permissão para validar uma conta de usuário.')

        current_time = TimeManipulation().get_current_time()

        if current_time > user.get('verification_email_code_expires_at'):
            raise InvalidParameter(parameter='Código de validação', body='expirado')

        if body.get('verification_email_code') != user.get('verification_email_code'):
            raise InvalidParameter(parameter='Código de validação', body='inválido')

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
            create_at=int(user.get('create_at')),
            verification_email_code=None,
            verification_email_code_expires_at=None,
            password_reset_code=user.get('password_reset_code'),
            password_reset_code_expires_at=user.get('password_reset_code_expires_at')
        )

        self.__user_interface.update_user(user)

        return None
