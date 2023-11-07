from typing import Dict
from bcrypt import checkpw

from src.shared.errors.modules_errors import *
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface


class GetTokenUseCase:
    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface
        self.__token = TokenAuthy()

    def __call__(self, body: Dict) -> Dict:
        if body.get('email') is None and body.get('access_key') is None:
            raise MissingParameter('Dado de acesso')

        if body.get('email') and body.get('access_key'):
            raise InvalidParameter('Dado de acesso', 'incorreto')

        if body.get('password') is None:
            raise MissingParameter('Password')

        if body.get('keep_login') is None:
            raise MissingParameter('Keep login')

        if body.get('email'):
            user = self.__user_interface.authenticate(email=body['email'])
        else:
            user = self.__user_interface.authenticate(access_key=body['access_key'])
        if not user:
            raise UserNotAuthenticated()

        if not checkpw(body['password'].encode('utf-8'), user['password'].encode('utf-8')):
            raise UserNotAuthenticated()

        token = self.__token.generate_token(user_id=user['user_id'], keep_login=body.get('keep_login'))

        return {"token": token}
