from typing import Dict
from src.shared.https_codes.https_code import *
from src.shared.errors.controller_errors import InvalidRequest, MissingParameter, InvalidParameter
from src.shared.errors.usecase_errors import DataAlreadyUsed
from .create_user_usecase import CreateUserUseCase
from .create_user_viewmodel import CreateUserViewModel


class CreateUserController:
    def __init__(self, usecase: CreateUserUseCase):
        self.__usecase = usecase
        self.__viewmodel = CreateUserViewModel()

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
                                                 phone=phone, password=password, accepted_terms=accepted_terms)

            response = self.__viewmodel(create_user_usecase)

            return Created(response)

        except DataAlreadyUsed as e:
            return BadRequest(e.body)

        except InvalidRequest as e:
            return BadRequest(e.body)

        except InvalidParameter as e:
            return BadRequest(e.body)

        except MissingParameter as e:
            return BadRequest(e.body)

        except Exception as e:
            return InternalServerError(e.args[0])















