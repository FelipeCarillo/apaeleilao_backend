from typing import Dict

from src.shared.structure.entities.user import User
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM
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
        if not body.get('verification_email_code') and not body.get('password_reset_code'):
            raise MissingParameter('verification_email_code ou password_reset_code')
        if body.get('verification_email_code') and body.get('password_reset_code'):
            raise InvalidParameter('verification_email_code ou password_reset_code',
                                   'não pode ser enviado os dois códigos ao mesmo tempo')

        decoded_token = self.__token.decode_token(auth['Authorization'])
        if not decoded_token:
            raise UserNotAuthenticated("Token de acesso inválido ou expirado.")
        user_id = decoded_token.get('user_id')
        user = self.__user_interface.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotAuthenticated()
        
        first_name = body.get("first_name", user.get("first_name"))
        last_name = body.get("last_name", user.get("last_name"))
        phone = body.get("phone", user.get("phone"))

        user = User(
            user_id=user["user_id"],
            first_name=first_name,
            last_name=last_name,
            cpf=user.get("cpf"),
            email=user.get("email"),
            phone=phone,
            password=user.get("password"),
            accepted_terms=user.get("accepted_terms"),
            status_account=user.get("status_account"),
            type_account=user.get("type_account"),
            date_joined=int(user.get("date_joined")),
            verification_email_code=int(user.get('verification_email_code')) 
            if user.get('verification_email_code') else None,
            verification_email_code_expires_at=int(user.get('verification_email_code_expires_at')) 
            if user.get('verification_email_code_expires_at') else None,
            password_reset_code=int(user.get('password_reset_code')) if user.get('password_reset_code') else None,
            password_reset_code_expires_at=int(user.get('password_reset_code_expires_at')) 
            if user.get('password_reset_code_expires_at') else None
        )

        return self.__user_interface.update_user(user)