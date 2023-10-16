import os
import uuid

from typing import Dict
from bcrypt import hashpw, gensalt

from src.shared.structure.entities.user import User
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.helper_functions.time_manipulation import TimeManipulation
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM, TYPE_ACCOUNT_USER_ENUM
from src.shared.errors.modules_errors import DataAlreadyUsed, MissingParameter, UserNotAuthenticated


class CreateUserUseCase:
    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface
        self.__token = TokenAuthy()
        self.__encrypt_key = os.getenv('ENCRYPT_KEY')
        self.__jwt_algorithm = os.getenv('JWT_ALGORITHM')

    def __call__(self, auth: Dict, body: Dict) -> Dict:

        if not body.get('email'):
            raise MissingParameter('Email')

        if not body.get('cpf'):
            raise MissingParameter('CPF')

        if self.__user_interface.get_user_by_email(body['email']):
            raise DataAlreadyUsed('Email')

        if self.__user_interface.get_user_by_cpf(body['cpf']):
            raise DataAlreadyUsed('CPF')

        type_account_need_permission = [TYPE_ACCOUNT_USER_ENUM.ADMIN, TYPE_ACCOUNT_USER_ENUM.MODERATOR]
        type_account = body.get('type_account', 'USER')
        status_account = STATUS_USER_ACCOUNT_ENUM.PENDING.value
        if TYPE_ACCOUNT_USER_ENUM(type_account) in type_account_need_permission:
            if not auth:
                raise MissingParameter('auth')
            if not auth.get('email'):
                raise MissingParameter('email')
            if not auth.get('password'):
                raise MissingParameter('password')
            auth = self.__user_interface.authenticate(email=auth['email'], password=auth['password'])
            if not auth:
                raise UserNotAuthenticated()
            if auth.get('type_account') != TYPE_ACCOUNT_USER_ENUM.ADMIN.value:
                raise UserNotAuthenticated()
            status_account = STATUS_USER_ACCOUNT_ENUM.ACTIVE.value

        user_id = str(uuid.uuid4())
        date_joined = TimeManipulation.get_current_time()

        user = User(user_id=user_id,
                    first_name=body.get('first_name'),
                    last_name=body.get('last_name'),
                    cpf=body.get('cpf'),
                    email=body.get('email'),
                    phone=body.get('phone'),
                    password=body.get('password'),
                    accepted_terms=body.get('accepted_terms'),
                    status_account=status_account,
                    type_account=type_account,
                    date_joined=date_joined)

        user.password = hashpw(user.password.encode('utf-8'), gensalt()).decode('utf-8')

        self.__user_interface.create_user(user.to_dict())

        token = self.__token.encode(user_id=user_id)

        return {"token": token}
