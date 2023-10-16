from typing import Dict

from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.errors.modules_errors import MissingParameter, UserNotAuthenticated


class GetTokenUseCase:
    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface
        self.__token = TokenAuthy()

    def __call__(self, body: Dict) -> Dict:
        if not body.get('email'):
            raise MissingParameter('Email')
        if not body.get('password'):
            raise MissingParameter('Password')
        user = self.__user_interface.authenticate(email=body['email'], password=body['password'])
        if not user:
            raise UserNotAuthenticated()

        token = self.__token.encode(user_id=user['user_id'])

        return {"token": token}
