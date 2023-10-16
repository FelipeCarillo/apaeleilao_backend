import os
import jwt
from abc import ABC
from typing import Dict

from src.shared.helper_functions.time_manipulation import TimeManipulation


class TokenAuthy(ABC):
    def __init__(self):
        self.__secret = os.environ.get('ENCRYPTED_KEY')

    def encode(self, user_id: str) -> str:
        date_exp = TimeManipulation().plus_day(30)
        return jwt.encode({"user_id": user_id, "exp": date_exp}, self.__secret,
                          algorithm='HS256')

    def decode(self, token: str) -> Dict:
        return jwt.decode(token, self.__secret, algorithms=['HS256'])