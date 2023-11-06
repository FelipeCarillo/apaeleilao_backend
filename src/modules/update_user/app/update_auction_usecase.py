from typing import Dict
from bcrypt import checkpw, hashpw, gensalt

from src.shared.structure.entities.user import User
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.errors.modules_errors import MissingParameter, UserNotAuthenticated, InvalidParameter


class UpdateUserUseCase:

    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface
        self.__token = TokenAuthy()

    def __call__(self, auth: Dict, body: Dict):
        if not auth:
            MissingParameter('auth')
        if not auth.get('Authorization'):
            MissingParameter('Authorization')

        if not body:
            MissingParameter('body')

        decoded_token = self.__token.decode_token(auth['Authorization'])
        if not decoded_token:
            raise UserNotAuthenticated("Token de acesso inválido ou expirado.")
        user_id = decoded_token.get('user_id')
        user = self.__user_interface.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotAuthenticated()

        if checkpw(body.get("password").encode("utf-8"), user.get("password").encode("utf-8")):
            raise InvalidParameter("Senha", "deve ser diferente da anterior")

        first_name = body.get("first_name", user.get("first_name")).title()
        last_name = body.get("last_name", user.get("last_name")).title()
        phone = body.get("phone", user.get("phone"))
        password = body.get("password", user.get("password"))

        user = User(
            user_id=user["user_id"],
            first_name=first_name,
            last_name=last_name,
            cpf=user.get("cpf"),
            email=user.get("email"),
            phone=phone,
            password=hashpw(password.encode("utf-8"), gensalt()).decode("utf-8"),
            accepted_terms=user.get("accepted_terms"),
            status_account=user.get("status_account"),
            type_account=user.get("type_account"),
            created_at=int(user.get("created_at")),
            verification_email_code=int(user.get('verification_email_code'))
            if user.get('verification_email_code') else None,
            verification_email_code_expires_at=int(user.get('verification_email_code_expires_at'))
            if user.get('verification_email_code_expires_at') else None,
        )

        return self.__user_interface.update_user(user)
