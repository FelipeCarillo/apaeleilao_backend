from typing import Dict
from jwt import ExpiredSignatureError, InvalidTokenError

from .confirm_email_code_usecase import ConfirmEmailCodeUsecase

from src.shared.https_codes.https_code import OK, BadRequest, InternalServerError, Unauthorized, ParameterError
from src.shared.errors.modules_errors import InvalidRequest, MissingParameter, InvalidParameter, UserNotAuthenticated


class ConfirmEmailCodeController:
    def __init__(self, usecase: ConfirmEmailCodeUsecase):
        self.__usecase = usecase

    def __call__(self, request: Dict):
        try:
            if not request:
                raise InvalidRequest()

            if not request['auth']:
                raise MissingParameter('auth')

            if not request['body']:
                raise MissingParameter('body')

            confirm_email_code_usecase = self.__usecase(auth=request['auth'], body=request['body'])

            return OK(body=confirm_email_code_usecase, message="Código confirmado com sucesso.")

        except ExpiredSignatureError:
            return Unauthorized(message="Token expirado.")

        except InvalidTokenError:
            return Unauthorized(message="Token inválido.")

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
