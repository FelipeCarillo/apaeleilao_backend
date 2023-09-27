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
        first_name = request['body']['first_name']
        last_name = request['body']['last_name']
        phone = request['body']['phone']
        password = request['body']['password']
        accepted_terms = request['body']['accepted_terms']

        create_user_usecase = self.__usecase(email=email, cpf=cpf, first_name=first_name, last_name=last_name,
                                             phone=phone, password=password, accepted_terms=accepted_terms,
                                             is_verified=False)
        return create_user_usecase









