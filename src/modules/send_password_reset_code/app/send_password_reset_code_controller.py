from typing import Dict

from .send_password_reset_code_usecase import SendPasswordResetCodeUseCase

from src.shared.https_codes.https_code import OK, BadRequest, InternalServerError, Unauthorized, ParameterError, \
    NotFound
from src.shared.errors.modules_errors import InvalidRequest, MissingParameter, InvalidParameter, UserNotAuthenticated, \
    DataNotFound


class SendPasswordResetCodeController:
    def __init__(self, usecase: SendPasswordResetCodeUseCase):
        self.__usecase = usecase

    def __call__(self, request: Dict):
        try:
            if not request:
                raise InvalidRequest()

            if not request.get('body'):
                raise MissingParameter('body')

            usecase = self.__usecase(body=request.get('body'))

            message = f"Código enviado com sucesso para o e-mail: {usecase.get('email')}."

            return OK(body=None, message=message)

        except InvalidRequest as e:
            return BadRequest(message=e.message)

        except DataNotFound as e:
            return NotFound(message=e.message)

        except MissingParameter as e:
            return BadRequest(message=e.message)

        except InvalidParameter as e:
            return ParameterError(message=e.message)

        except UserNotAuthenticated as e:
            return Unauthorized(message=e.message)

        except Exception as e:
            return InternalServerError(message=e.args[0])

