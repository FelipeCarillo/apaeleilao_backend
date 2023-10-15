import os
import uuid
from typing import Dict
from bcrypt import hashpw, gensalt

from src.shared.structure.entities.user import User
from src.shared.errors.modules_errors import DataAlreadyUsed, MissingParameter, UserNotAuthenticated
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM, TYPE_ACCOUNT_USER_ENUM
from src.shared.structure.interface.user_interface import UserInterface


class AuthentificateUserUseCase:
    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface

    def __call__(self, auth: Dict, body: Dict) -> Dict:

        if not body.get("email"):
            raise MissingParameter("Email")
        
        if not body.get("password"):
            raise MissingParameter("Password")
        
        type_account_need_permission = [TYPE_ACCOUNT_USER_ENUM.ADMIN, TYPE_ACCOUNT_USER_ENUM.MODERATOR]
        type_account = body.get('type_account', 'USER')
        if TYPE_ACCOUNT_USER_ENUM(type_account) in type_account_need_permission:
            if not auth:
                raise MissingParameter('auth')
            if not auth.get('email'):
                raise MissingParameter('email')
            if not auth.get('password'):
                raise MissingParameter('password')
            auth = self.__user_interface.authenticate(email=auth['email'], password=auth['password'])
            if not auth:
                raise UserNotAuthenticated()
            if auth.get('type_account') != TYPE_ACCOUNT_USER_ENUM.ADMIN.value:
                raise UserNotAuthenticated()
            status_account = "ACTIVE"

        return self.__user_interface.authenticate(user_id = str(uuid.uuid4()), 
                                                  email=body.get("email"), 
                                                  password=body.get("password"),
                                                  password_hash=hashpw(body.get("password").encode('utf-8'), gensalt()).decode('utf-8'))