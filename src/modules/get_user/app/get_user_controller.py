from typing import Dict

from .get_user_usecase import GetUserUseCase
from .get_user_viewmodel import GetUserViewModel

from src.shared.https_codes.https_code import OK, BadRequest, InternalServerError, Unauthorized, ParameterError
from src.shared.errors.modules_errors import InvalidRequest, MissingParameter, InvalidParameter, UserNotAuthenticated


class GetUserController:
    def __init__(self, usecase: GetUserUseCase):
        self.__usecase = usecase
        self.__viewmodel = GetUserViewModel()

    def __call__(self, request: Dict):
        try:
            if not request:
                raise InvalidRequest()

            if not request.get('body'):
                raise MissingParameter('body')

            get_user_usecase = self.__usecase(body=request.get('body'))

            response = self.__viewmodel(get_user_usecase)

            return OK(body=response, message='Usuário encontrado com sucesso.')

        except UserNotAuthenticated as e:
            return Unauthorized(message=e.message)

        except InvalidRequest as e:
            return BadRequest(message=e.message)

        except InvalidParameter as e:
            return ParameterError(message=e.message)

        except MissingParameter as e:
            return BadRequest(message=e.message)

        except Exception as e:
            return InternalServerError(message=e.args[0])
