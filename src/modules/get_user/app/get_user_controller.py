from typing import Dict
from src.shared.https_codes.https_code import OK, BadRequest, InternalServerError, Unauthorized
from src.shared.errors.controller_errors import InvalidRequest, MissingParameter, InvalidParameter, UserNotAuthenticated
from src.shared.errors.usecase_errors import DataAlreadyUsed
from .get_user_usecase import GetUserUseCase
from .get_user_viewmodel import GetUserViewModel


class GetUserController:
    def __init__(self, usecase: GetUserUseCase):
        self.__usecase = usecase
        self.__viewmodel = GetUserViewModel()

    def __call__(self, request: Dict):
        try:
            if not request:
                raise InvalidRequest()

            if not request['body']:
                raise MissingParameter('body')

            user_id = request['body'].get('user_id', None)
            email = request['body'].get('email', None)
            password = request['body']['password']

            get_user_usecase = self.__usecase(email=email, password=password, user_id=user_id)

            response = self.__viewmodel(get_user_usecase)

            return OK(response)

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
