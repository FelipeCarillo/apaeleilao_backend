from typing import Dict

from src.shared.structure.entities.user import User
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM
from src.shared.errors.modules_errors import MissingParameter, UserNotAuthenticated


class GetUserUseCase:
    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface

    def __call__(self, body: Dict) -> User:
        if not body.get('email'):
            raise MissingParameter('email')
        if not body.get('password'):
            raise MissingParameter('password')

        auth = self.__user_interface.authenticate(email=body['email'], password=body['password'])
        if not auth:
            raise UserNotAuthenticated()

        status_account_permitted = [STATUS_USER_ACCOUNT_ENUM.ACTIVE, STATUS_USER_ACCOUNT_ENUM.PENDING,
                                    STATUS_USER_ACCOUNT_ENUM.SUSPENDED, STATUS_USER_ACCOUNT_ENUM.BANED]

        if STATUS_USER_ACCOUNT_ENUM(auth.get('status_account')) not in status_account_permitted:
            raise UserNotAuthenticated(message='Conta de usuário deletada.')

        user = User(
            user_id=auth['user_id'],
            first_name=auth.get('first_name'),
            last_name=auth.get('last_name'),
            cpf=auth.get('cpf'),
            email=auth.get('email'),
            phone=auth.get('phone'),
            password=auth.get('password'),
            accepted_terms=auth.get('accepted_terms'),
            status_account=auth.get('status_account'),
            suspensions=auth.get('suspensions'),
            date_joined=int(auth.get('date_joined')) if auth.get('date_joined') else None,
            verification_email_code=int(auth.get('verification_email_code')) if auth.get(
                'verification_email_code') else None,
            verification_email_code_expires_at=int(auth.get('verification_email_code_expires_at')) if auth.get(
                'verification_email_code_expires_at') else None,
            password_reset_code=int(auth.get('password_reset_code')) if auth.get('password_reset_code') else None,
            password_reset_code_expires_at=int(auth.get('password_reset_code_expires_at')) if auth.get(
                'password_reset_code_expires_at') else None
        )

        return user
