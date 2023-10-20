from typing import Dict

from src.shared.errors.modules_errors import *
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface


class GetTokenUseCase:
    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface
        self.__token = TokenAuthy()

    def __call__(self, body: Dict) -> Dict:
        if not body.get('email') and not body.get('access_key'):
            raise MissingParameter('Dado de acesso')

        if body.get('email') and body.get('access_key'):
            raise InvalidParameter('Dado de acesso', 'incorreto')

        if not body.get('password'):
            raise MissingParameter('Password')

        if body.get('email'):
            user = self.__user_interface.authenticate(email=body['email'], password=body['password'])
        else:
            user = self.__user_interface.authenticate(access_key=body['access_key'], password=body['password'])

        if not user:
            raise UserNotAuthenticated()
        token = self.__token.generate_token(user_id=user['user_id'], keep_login=True if body.get("keep_login") else False)

        return {"token": token}
