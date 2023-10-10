from typing import Dict

from .create_user_usecase import CreateUserUseCase
from .create_user_viewmodel import CreateUserViewModel

from src.shared.https_codes.https_code import Created, BadRequest, InternalServerError, ParameterError
from src.shared.errors.modules_errors import InvalidRequest, MissingParameter, InvalidParameter, DataAlreadyUsed


class CreateUserController:
    def __init__(self, usecase: CreateUserUseCase):
        self.__usecase = usecase
        self.__viewmodel = CreateUserViewModel()

    def __call__(self, request: Dict):
        try:
            if not request:
                raise InvalidRequest()

            if not request.get('body'):
                raise MissingParameter('body')

            create_user_usecase = self.__usecase(request=request['body'])

            response = self.__viewmodel(create_user_usecase)

            return Created(response, message='Usuário criado com sucesso.')

        except DataAlreadyUsed as e:
            return ParameterError(message=e.message)

        except InvalidRequest as e:
            return BadRequest(message=e.message)

        except InvalidParameter as e:
            return ParameterError(message=e.message)

        except MissingParameter as e:
            return BadRequest(message=e.message)

        except Exception as e:
            return InternalServerError(message=e.args[0])
