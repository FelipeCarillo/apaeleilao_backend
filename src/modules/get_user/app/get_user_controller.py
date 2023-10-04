from typing import Dict
from src.shared.https_codes.https_code import OK, BadRequest, InternalServerError, Unauthorized
from src.shared.errors.controller_errors import InvalidRequest, MissingParameter, InvalidParameter, UserNotAuthenticated
from src.shared.errors.usecase_errors import DataAlreadyUsed
from .get_user_usecase import GetUserUseCase


class GetUserController:
    def __init__(self, usecase: GetUserUseCase):
        self.__usecase = usecase

    def __call__(self, request: Dict):
        try:
            if not request:
                raise InvalidRequest()

            if not request['body']:
                raise MissingParameter('body')

            email = request['body']['email']
            password = request['body']['password']

            get_user_usecase = self.__usecase(email=email, password=password)
            return OK(get_user_usecase)

        except UserNotAuthenticated as e:
            return Unauthorized(e.body)

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