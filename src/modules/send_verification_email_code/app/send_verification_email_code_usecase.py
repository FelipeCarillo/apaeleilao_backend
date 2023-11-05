import os
import random
import smtplib
import datetime
from typing import Dict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.shared.structure.entities.user import User
from src.shared.helper_functions.email_function import Email
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM, TYPE_ACCOUNT_USER_ENUM
from src.shared.helper_functions.time_manipulation import TimeManipulation
from src.shared.errors.modules_errors import MissingParameter, UserNotAuthenticated, InvalidParameter


class SendVerificationEmailCodeUseCase:

    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface
        self.__token = TokenAuthy()
        self.__email = Email()

    def __call__(self, auth: Dict):
        if not auth.get('Authorization'):
            MissingParameter('Authorization')

        decoded_token = self.__token.decode_token(auth['Authorization'])
        if not decoded_token:
            raise UserNotAuthenticated("Token de acesso inválido ou expirado.")

        user_id = decoded_token.get('user_id')
        user = self.__user_interface.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotAuthenticated()

        status_account_permitted = [STATUS_USER_ACCOUNT_ENUM.PENDING]
        if STATUS_USER_ACCOUNT_ENUM(user.get('status_account')) not in status_account_permitted:
            raise UserNotAuthenticated(message='Conta de usuário já validada.')

        if TYPE_ACCOUNT_USER_ENUM(user.get('type_account')) != TYPE_ACCOUNT_USER_ENUM.USER:
            raise UserNotAuthenticated(message='Você não tem permissão para validar uma conta de usuário.')

        code = random.randint(10000, 99999)
        code_expires_at = TimeManipulation().plus_minute(1.5)

        user = User(user_id=user['user_id'],
                    first_name=user['first_name'],
                    last_name=user['last_name'],
                    cpf=user['cpf'],
                    email=user['email'],
                    phone=user['phone'],
                    password=user['password'],
                    accepted_terms=user['accepted_terms'],
                    status_account=user['status_account'],
                    type_account=user['type_account'],
                    created_at=int(user['created_at']),
                    verification_email_code=str(code),
                    verification_email_code_expires_at=code_expires_at,
                    )

        datetime_expire = datetime.datetime.fromtimestamp(code_expires_at).strftime(
            "%d/%m/%Y %H:%M:%S")
        self.__user_interface.update_user(user)

        email_content = f"""
        <div class="TextsBox" style="word-wrap: break-word;">
          <h2 style="color: #949393;">Obrigado, {user.first_name}<p>Aqui está o seu código de validação do email:</p></h2>
          <h4 style="color: #000000; font-size: 26px; letter-spacing: 10px;">{user.verification_email_code}</h4>
          <h4 style="color: #000000;">Código válido até: {datetime_expire}</h4>
        </div>
        """

        self.__email.set_email_template(title="Código de Validação", content=email_content)

        self.__email.send_email(
            to=user.email,
            subject="Código de Validação.",
        )

        return {"email": user.email, 'code_expires_at': code_expires_at}
