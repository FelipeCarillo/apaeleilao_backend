from typing import Dict

from .create_auction_usecase import CreateUserUseCase

from src.shared.https_codes.https_code import Created, BadRequest, InternalServerError, ParameterError, Unauthorized
from src.shared.errors.modules_errors import InvalidRequest, MissingParameter, InvalidParameter, DataAlreadyUsed, \
    UserNotAuthenticated


class CreateUserController:
    def __init__(self, usecase: CreateUserUseCase):
        self.__usecase = usecase

    def __call__(self, request: Dict):
        try:
            if not request:
                raise InvalidRequest()

            if not request.get('body'):
                raise MissingParameter('body')

            usecase = self.__usecase(auth=request.get('auth'), body=request.get('body'))

            return Created(usecase, message='Leilão criado com sucesso.')

        except DataAlreadyUsed as e:
            return ParameterError(message=e.message)

        except InvalidRequest as e:
            return BadRequest(message=e.message)

        except InvalidParameter as e:
            return ParameterError(message=e.message)

        except MissingParameter as e:
            return BadRequest(message=e.message)

        except UserNotAuthenticated as e:
            return Unauthorized(message=e.message)

        except Exception as e:
            return InternalServerError(message=e.args[0])
