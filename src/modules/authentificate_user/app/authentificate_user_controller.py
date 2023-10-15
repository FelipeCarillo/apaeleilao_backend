from typing import Dict

from .authentificate_user_usecase import AuthentificateUserUseCase
from .authentificate_user_viewmodel import AuthentificateUserViewModel

from src.shared.https_codes.https_code import Created, BadRequest, InternalServerError, ParameterError, Unauthorized
from src.shared.errors.modules_errors import InvalidRequest, MissingParameter, InvalidParameter, DataAlreadyUsed, \
    UserNotAuthenticated


class AuthentificateUserController:
    def __init__(self, usecase: AuthentificateUserUseCase):
        
        self.__usecase = usecase
        self.__viewmodel = AuthentificateUserViewModel()

    def __call__(self, request: Dict):
        try:
            if not request:
                raise InvalidRequest()

            if not request.get('body'):
                raise MissingParameter('body')

            authentificate_user_usecase = self.__usecase(auth=request.get('auth'), body=request.get('body'))

            response = self.__viewmodel(authentificate_user_usecase)

            return Created(response, message='Usuário criado com sucesso.')

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

