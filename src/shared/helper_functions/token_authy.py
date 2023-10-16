import os
import jwt
from abc import ABC
from typing import Dict
from jwt import ExpiredSignatureError, InvalidTokenError

from src.shared.helper_functions.time_manipulation import TimeManipulation


class TokenAuthy(ABC):
    def __init__(self):
        self.__secret = os.environ.get('ENCRYPTED_KEY')

    def generate_token(self, user_id: str, keep_login: bool = True) -> str:
        if keep_login:
            date_exp = TimeManipulation().plus_day(30)
        else:
            date_exp = TimeManipulation().plus_hour(1)
        return jwt.encode({"user_id": user_id, "exp": date_exp}, self.__secret,
                          algorithm='HS256')

    def decode_token(self, token: str) -> Dict or None:
        try:
            decoded_token = jwt.decode(token, self.__secret, algorithms=['HS256'])
            return decoded_token
        except ExpiredSignatureError:
            return None
        except InvalidTokenError:
            return None
