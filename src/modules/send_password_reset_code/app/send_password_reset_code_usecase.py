import os
import random
import datetime
from typing import Dict

from src.shared.structure.entities.user import User
from src.shared.helper_functions.email_function import Email
from src.shared.errors.modules_errors import MissingParameter
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.helper_functions.time_manipulation import TimeManipulation


class SendPasswordResetCodeUseCase:
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
        url = f"https://{self.__domain}/reset-password?token={token}"

        email_format = f"""
        <html lang="pt-br" charset="UTF-8">
        <head>
        </head>
        <body
            style="margin: 0; padding: 0; display: flex; align-items: center; justify-content: center; min-height: 75vh; background-color: white; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;">
            <table class="main"
                style="width: 50vw; max-width: 600px; background-color: #E9E9E9; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25); overflow: hidden;">
                <tr>
                    <td>
                        <table class="TittleBox" style="width: 100%; background-color: #2C4FBC; border-radius: 10px 10px 0 0;">
                            <tr>
                                <td style="text-align: center; padding: 20px;">
                                    <img alt="Apae Leilão Logo"
                                        src="https://apaeleilaoimtphotos.s3.sa-east-1.amazonaws.com/logo-apaeleilao/logo-apaeleilao-branco.jpg" 
                                        style="width: 50%;"/>
                                    <h1 style="color: #FFFFFF; margin-top: 10px;"><b>Redefinir Senha!</b></h1>
                                </td>
                            </tr>
                        </table>
                        <table class="ContentBox" style="width: 100%; background-color: #FFFFFF;">
                            <tr>
                                <td style="text-align: center; padding: 20px;">
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
                                </td>
                            </tr>
                        </table>
                        <table class="BottomBox"
                            style="width: 100%; background-color: #FFFFFF; border-top: 1px solid gray; border-radius: 0 0 10px 10px;">
                            <tr>
                                <td style="text-align: center; padding: 20px;">
                                    <div class="TextsBox" style="color: #949393; word-wrap: break-word;">
                                        <h2>Atenciosamente,</h2>
                                        <h2><b>IMT</b></h2>
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        self.__email.send_email(
            to=user.get('email'),
            subject="Redefinir Senha.",
            body=email_format
        )

        return user.get('email')
