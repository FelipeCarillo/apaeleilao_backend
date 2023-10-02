from typing import Dict
from src.shared.https_codes.https_code import *
from src.shared.errors.controller_errors import InvalidRequest, MissingParameter
from create_user_usecase import CreateUserUseCase


class CreateUserController:
    def __init__(self, usecase: CreateUserUseCase):
        self.__usecase = usecase

    def __call__(self, request: Dict):
        try:
            if not request:
                raise InvalidRequest()

            if not request['body']:
                raise MissingParameter('body')

            email = request['body']['email']
            cpf = request['body']['cpf']
            first_name = request['body']['first_name']
            last_name = request['body']['last_name']
            phone = request['body']['phone']
            password = request['body']['password']
            accepted_terms = request['body']['accepted_terms']

            create_user_usecase = self.__usecase(email=email, cpf=cpf, first_name=first_name, last_name=last_name,
                                                 phone=phone, password=password, accepted_terms=accepted_terms,
                                                 is_verified=False)
            return create_user_usecase

        except InvalidRequest as e:
            return BadRequest(e)

        except MissingParameter as e:
            return BadRequest(e)

        except Exception as e:
            return InternalServerError(e)















