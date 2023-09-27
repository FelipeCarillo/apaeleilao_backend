from typing import Dict
from .create_user_usecase import CreateUserUseCase


class CreateUserController:
    def __init__(self, usecase: CreateUserUseCase):
        self.__usecase = usecase

    def __call__(self, request: Dict):
        if not request:
            raise {
                'statusCode': 400,
                'body': 'Invalid request'
            }
        if not request['body']:
            raise {
                'statusCode': 400,
                'body': 'Invalid request body'
            }

        email = request['body']['email']
        cpf = request['body']['cpf']
        user_id = request['body']['user_id']
        first_name = request['body']['first_name']
        last_name = request['body']['last_name']
        password = request['body']['password']
        accept_terms = request['body']['accept_terms']
        is_verified = request['body']['is_verified']

        create_user_usecase = self.__usecase(email, cpf, user_id, first_name, last_name,
                                             password, accept_terms)
        return create_user_usecase









