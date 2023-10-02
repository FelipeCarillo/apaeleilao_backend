import uuid
from time import time_ns
from random import randint
from src.shared.https_codes.https_code import *
from src.shared.structure.entities.user import User
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.errors.usecase_errors import DataAlreadyUsed


class CreateUserUseCase:
    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface

    def __call__(self, email: str, cpf: str, first_name: str, last_name: str, password: str, phone: str, accepted_terms: bool,
                 is_verified: bool):
        try:
            data_duplicated = []
            if self.__user_interface.get_user_by_email(email):
                data_duplicated.append('Email')

            if self.__user_interface.get_user_by_cpf(cpf):
                data_duplicated.append('CPF')

            if len(data_duplicated) > 0:
                raise DataAlreadyUsed(data_duplicated)

            cpf = cpf.replace(".", "").replace("-", "")

            user_id = str(uuid.uuid4())
            date_joined = time_ns()
            verification_code = randint(10000, 99999)
            verification_code_expires_at = time_ns() + 3600

            user = User(user_id=user_id, email=email, cpf=cpf, first_name=first_name, last_name=last_name,
                        password=password, phone=phone, accepted_terms=accepted_terms, is_verified=is_verified,
                        date_joined=date_joined, verification_code=verification_code,
                        verification_code_expires_at=verification_code_expires_at)

            return self.__user_interface.create_user(user)

        except DataAlreadyUsed as e:
            return BadRequest(e)

        except Exception as e:
            return InternalServerError(e)
