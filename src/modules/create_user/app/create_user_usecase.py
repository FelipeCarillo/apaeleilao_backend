import uuid
from time import time
from random import randint
from typing import Dict

from src.shared.structure.entities.user import User
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM
from src.shared.errors.usecase_errors import DataAlreadyUsed
from src.shared.structure.interface.user_interface import UserInterface


class CreateUserUseCase:
    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface

    def __call__(self, email: str, cpf: str, first_name: str, last_name: str, password: str, phone: str,
                 accepted_terms: bool) -> Dict:

        if self.__user_interface.get_user_by_email(email):
            raise DataAlreadyUsed('email')

        if self.__user_interface.get_user_by_cpf(cpf):
            raise DataAlreadyUsed('cpf')

        user_id = str(uuid.uuid4())
        status_account = STATUS_USER_ACCOUNT_ENUM.PENDING
        suspensions = []
        date_joined = int(time())

        user = User(user_id=user_id, first_name=first_name, last_name=last_name, cpf=cpf, email=email, phone=phone,
                    password=password, accepted_terms=accepted_terms, status_account=status_account,
                    suspensions=suspensions, date_joined=date_joined)

        return self.__user_interface.create_user(user)
