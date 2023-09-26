from typing import Dict
from .create_user_usecase import CreateUserUseCase


class CreateUserController:
    def __init__(self, request: Dict):
        self.__request = request

    def __call__(self):
        if not self.__request:
            raise {
                'statusCode': 400,
                'body': 'Invalid request'
            }
        if not self.__request['body']:
            raise {
                'statusCode': 400,
                'body': 'Invalid request body'
            }
        if not self.__request['auth']:
            raise {
                'statusCode': 400,
                'body': 'Invalid request auth'
            }
        create_user_usecase = CreateUserUseCase(self.__request)()
        return create_user_usecase









