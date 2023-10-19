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

    def __call__(self, body: Dict) -> Dict:

        if not body.get('email'):
            raise MissingParameter('Email')

        if not body.get('cpf'):
            raise MissingParameter('CPF')

        if self.__user_interface.get_user_by_email(body['email']):
            raise DataAlreadyUsed('Email')

        if self.__user_interface.get_user_by_cpf(body['cpf']):
            raise DataAlreadyUsed('CPF')

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
                    suspensions=[],
                    status_account=STATUS_USER_ACCOUNT_ENUM.PENDING.value,
                    type_account=TYPE_ACCOUNT_USER_ENUM.USER.value,
                    date_joined=date_joined
                    )

        user.password = hashpw(user.password.encode('utf-8'), gensalt()).decode('utf-8')

        token = self.__token.generate_token(user_id=user_id, keep_login=True)

        self.__user_interface.create_user(user.to_dict())

        return {"token": token}
