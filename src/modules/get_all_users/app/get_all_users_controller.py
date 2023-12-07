from .get_all_users_usecase import GetAllUsersUseCase

from src.shared.errors.modules_errors import *
from src.shared.https_codes.https_code import *


class GetAllUsersController:
    def __init__(self, usecase: GetAllUsersUseCase):
        self.__usecase = usecase

    def __call__(self, request: Dict):
        try:
            if not request:
                raise InvalidRequest()

            if not request.get('auth'):
                raise MissingParameter('auth')

            usecase = self.__usecase(auth=request.get('auth'))

            return OK(body=usecase, message="Usuários encontrados com sucesso.")

        except DataNotFound as e:
            return NotFound(message=e.message)

        except InvalidRequest as e:
            return BadRequest(message=e.message)

        except UserNotAuthenticated as e:
            return Unauthorized(message=e.message)

        except InvalidParameter as e:
            return ParameterError(message=e.message)

        except MissingParameter as e:
            return BadRequest(message=e.message)

        except Exception as e:
            return InternalServerError(message=e.args[0])
