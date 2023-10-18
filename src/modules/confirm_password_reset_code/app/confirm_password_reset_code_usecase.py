from typing import Dict

from src.shared.structure.entities.user import User
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.helper_functions.time_manipulation import TimeManipulation
from src.shared.errors.modules_errors import MissingParameter, UserNotAuthenticated, InvalidParameter


class ConfirmPasswordResetCodeUseCase:

    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface
        self.__token = TokenAuthy()

    def __call__(self, auth: Dict, body: Dict):
        if not auth:
            raise MissingParameter('auth')
        if not auth.get('Authorization'):
            raise MissingParameter('Authorization')

        if not body:
            raise MissingParameter('body')
        if not body.get('password_reset_code'):
            raise MissingParameter('Código de redefinição')

        decoded_token = self.__token.decode_token(token=auth.get("Authorization"))
        if not decoded_token:
            raise UserNotAuthenticated("Token de acesso inválido ou expirado.")
        email = decoded_token.get('user_id')

        user = self.__user_interface.get_user_by_email(email=email)
        if not user:
            raise UserNotAuthenticated()

        current_time = TimeManipulation().get_current_time()

        if current_time > user.get('password_reset_code_expires_at'):
            raise InvalidParameter(parameter='Código de redefinição', body='expirado')

        if body.get('password_reset_code') != user.get('password_reset_code'):
            raise InvalidParameter(parameter='Código de redefinição', body='inválido')

        user = User(
            user_id=user.get('user_id'),
            first_name=user.get('first_name'),
            last_name=user.get('last_name'),
            cpf=user.get('cpf'),
            email=user.get('email'),
            phone=user.get('phone'),
            password=user.get('password'),
            accepted_terms=user.get('accepted_terms'),
            suspensions=user.get('suspensions'),
            status_account=user.get('status_account'),
            type_account=user.get('type_account'),
            date_joined=int(user.get('date_joined')),
            verification_email_code=user.get('verification_email_code'),
            verification_email_code_expires_at=user.get('verification_email_code_expires_at'),
            password_reset_code=None,
            password_reset_code_expires_at=None
        )

        return {
            'token': self.__token.generate_token(user_id=user.user_id),
        }