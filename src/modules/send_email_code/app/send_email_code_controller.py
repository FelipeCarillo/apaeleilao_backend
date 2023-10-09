from typing import Dict

from .send_email_code_usecase import SendEmailCodeUseCase

from src.shared.https_codes.https_code import OK, BadRequest, InternalServerError, Unauthorized, ParameterError
from src.shared.errors.modules_errors import InvalidRequest, MissingParameter, InvalidParameter, UserNotAuthenticated


class SendEmailCodeController:
    def __init__(self, usecase: SendEmailCodeUseCase):
        self.__usecase = usecase

    def __call__(self, request: Dict):
        try:
            if not request:
                raise InvalidRequest()

            if not request['auth']:
                raise MissingParameter('auth')

            send_email_code_usecase = self.__usecase(auth=request['auth'])

            return OK(body=send_email_code_usecase['body'], message="Código enviado com sucesso.")

        except InvalidRequest as e:
            return BadRequest(message=e.message)

        except MissingParameter as e:
            return BadRequest(message=e.message)

        except InvalidParameter as e:
            return ParameterError(message=e.message)

        except UserNotAuthenticated as e:
            return Unauthorized(message=e.message)

        except Exception as e:
            return InternalServerError(message=e.args[0])

