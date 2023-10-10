from typing import Dict

from src.shared.structure.entities.user import User
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM
from src.shared.errors.modules_errors import MissingParameter, UserNotAuthenticated


class GetUserUseCase:
    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface

    def __call__(self, request: Dict) -> User:
        if not request.get('email'):
            raise MissingParameter('email')
        if not request.get('password'):
            raise MissingParameter('password')

        auth = self.__user_interface.authenticate(email=request['email'], password=request['password'])
        if not auth:
            raise UserNotAuthenticated()

        status_account_permitted = [STATUS_USER_ACCOUNT_ENUM.ACTIVE, STATUS_USER_ACCOUNT_ENUM.PENDING,
                                    STATUS_USER_ACCOUNT_ENUM.SUSPENDED, STATUS_USER_ACCOUNT_ENUM.BANED]

        if STATUS_USER_ACCOUNT_ENUM(auth['status_account']) not in status_account_permitted:
            raise UserNotAuthenticated(message='Conta de usuário deletada.')

        date_joined = int(auth['date_joined']) if auth['date_joined'] else None
        verification_email_code = int(auth['verification_email_code']) if auth['verification_email_code'] else None
        verification_email_code_expires_at = int(auth['verification_email_code_expires_at']) if auth['verification_email_code_expires_at'] else None
        password_reset_code = int(auth['password_reset_code']) if auth['password_reset_code'] else None
        password_reset_code_expires_at = int(auth['password_reset_code_expires_at']) if auth['password_reset_code_expires_at'] else None

        user = User(user_id=auth['user_id'], first_name=auth['first_name'], last_name=auth['last_name'], cpf=auth['cpf'], email=auth['email'],
                    phone=auth['phone'], password=auth['password'], accepted_terms=auth['accepted_terms'],
                    status_account=auth['status_account'], suspensions=auth['suspensions'],
                    date_joined=date_joined,
                    verification_email_code=verification_email_code,
                    verification_email_code_expires_at=verification_email_code_expires_at,
                    password_reset_code=password_reset_code,
                    password_reset_code_expires_at=password_reset_code_expires_at)

        return user
