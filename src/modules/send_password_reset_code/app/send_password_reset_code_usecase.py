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
    TIME_EXPIRE = 1.5

    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface
        self.__token = TokenAuthy()
        self.__email = Email()

    def __call__(self, body: Dict):
        if not body.get('email'):
            MissingParameter('Email')

        user = self.__user_interface.get_user_by_email(email=body.get('email'))
        if not user:
            return {'email': body.get('email')}

        code = random.randint(10000, 99999)
        code_expires_at = TimeManipulation().plus_minute(self.TIME_EXPIRE)

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
                    date_joined=int(user['date_joined']),
                    verification_email_code=user['verification_email_code'],
                    verification_email_code_expires_at=user['verification_email_code_expires_at'],
                    password_reset_code=str(code),
                    password_reset_code_expires_at=code_expires_at
                    )

        datetime_expire = datetime.datetime.fromtimestamp(code_expires_at).strftime(
            "%d/%m/%Y %H:%M:%S")
        self.__user_interface.update_user(user)

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
                                    <h1 style="color: #FFFFFF; margin-top: 10px;"><b>Código de Redefinir Senha!</b></h1>
                                </td>
                            </tr>
                        </table>
                        <table class="ContentBox" style="width: 100%; background-color: #FFFFFF;">
                            <tr>
                                <td style="text-align: center; padding: 20px;">
                                    <div class="TextsBox" style="word-wrap: break-word;">
                                        <h2 style="color: #949393;">Obrigado, {user.first_name}<p>Aqui está o seu código de redefinição de senha:</p>
                                        </h2>
                                        <h4 style="color: #000000; font-size: 26px; letter-spacing: 10px;">{user.password_reset_code}</h4>
                                        <h4 style="color: #000000;">Codigo válido até: {datetime_expire}</h4>
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
                                        <h2><b>APAE São Caetano do Sul - IMT</b></h2>
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
            to=user.email,
            subject="Código de Redefinir Senha.",
            body=email_format
        )

        code_expires_at = int(TimeManipulation(code_expires_at).plus_hour(3))

        return {
                'email': user.email,
                'token': self.__token.generate_token(user_id=user.email, exp_time=code_expires_at),
                'code_expires_at': code_expires_at
                }
