import os
import datetime
from typing import Dict

from src.shared.helper_functions.email_function import Email
from src.shared.errors.modules_errors import MissingParameter
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.helper_functions.time_manipulation import TimeManipulation


class SendResetPasswordLinkUseCase:
    TIME_EXPIRE = 15  # minutes

    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface
        self.__token = TokenAuthy()
        self.__email = Email()
        self.__domain = os.environ.get("DOMAIN", "")

    def __call__(self, body: Dict):
        if not body.get('email'):
            MissingParameter('Email')

        user = self.__user_interface.get_user_by_email(email=body.get('email'))
        if not user:
            return body.get('email')

        code_expires_at = TimeManipulation().plus_minute(self.TIME_EXPIRE)
        datetime_expire = datetime.datetime.fromtimestamp(code_expires_at).strftime(
            "%d/%m/%Y %H:%M:%S")

        token = self.__token.generate_token(user_id=user.get('user_id'), exp_time=code_expires_at)
        url = f"https://{self.__domain}/redefinirSenha?token={token}"

        email_content = f"""
            <div class="TextsBox" style="word-wrap: break-word;">
              <h2 style="color: #949393;">Obrigado, {user.get('first_name')}
                <p>
                  Clique no botão abaixo para ser direcionado a página de redefinição de senha:
                </p> 
              </h2>
              <a href="{url}" style="background-color: #0074d9; color: #fff; padding: 10px
                20px; text-decoration: none; border: none; border-radius: 5px; font-size: 
                larger">Redefinir Senha
              </a> 
              <h4 style="color: #000000;">Link válido até: {datetime_expire}</h4>
            </div>
        """

        self.__email.set_email_template(title="Redefinir Senha", content=email_content)

        self.__email.send_email(
            to=user.get('email'),
            subject="Redefinir Senha.",
            body=self.__email.email_body
        )

        return user.get('email')
