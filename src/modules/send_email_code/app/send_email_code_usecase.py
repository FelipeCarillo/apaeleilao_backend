import os
import time
import boto3
import random
import datetime
from typing import Dict

from src.shared.structure.entities.user import User
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.errors.modules_errors import MissingParameter, UserNotAuthenticated


class SendEmailCodeUseCase:

    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface
        self.__client = boto3.client('ses', region_name=os.environ.get('SES_REGION'))

    def __call__(self, auth: Dict):
        if not auth:
            MissingParameter('auth')
        if not auth.get('email'):
            MissingParameter('email')
        if not auth.get('password'):
            MissingParameter('password')

        auth = self.__user_interface.authenticate(email=auth['email'], password_hash=auth['password'])
        if not auth:
            raise UserNotAuthenticated()

        verification_email_code = random.randint(10000, 99999)
        verification_email_code_expires_at = int(time.time()) - 2 * 3600

        user = User(user_id=auth['user_id'], first_name=auth['first_name'], last_name=auth['last_name'],
                    cpf=auth['cpf'], email=auth['email'], phone=auth['phone'], password=auth['password'],
                    accepted_terms=auth['accepted_terms'], status_account=auth['status_account'],
                    suspensions=auth['suspensions'], date_joined=int(auth['date_joined']),
                    verification_email_code=verification_email_code,
                    verification_email_code_expires_at=verification_email_code_expires_at,
                    password_reset_code=auth['password_reset_code'],
                    password_reset_code_expires_at=auth['password_reset_code_expires_at'])

        datetime_expire = datetime.datetime.fromtimestamp(verification_email_code_expires_at).strftime(
            "%d/%m/%Y %H:%M:%S")
        self.__user_interface.update_user(user)

        email_format = f"""
        <!DOCTYPE html>
        <html lang="pt-br" charset="UTF-8">
        
        <head>
            <meta http-equiv="Content-Type" content="text/html charset=UTF-8" />
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
                                    <h1 style="color: #FFFFFF; margin-top: 10px;"><b>Código de Validação!</b></h1>
                                </td>
                            </tr>
                        </table>
                        <table class="ContentBox" style="width: 100%; background-color: #FFFFFF;">
                            <tr>
                                <td style="text-align: center; padding: 20px;">
                                    <div class="TextsBox" style="word-wrap: break-word;">
                                        <h2 style="color: #949393;">Obrigado, {user.first_name}<p>Aqui está o seu código de validação do email:</p>
                                        </h2>
                                        <h4 style="color: #000000; font-size: 26px; letter-spacing: 10px;">{user.verification_email_code}</h4>
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
                                        <h2><b>APAE São Caetano do Sul</b></h2>
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

        self.__client.send_email(
            Destination={
                'ToAddresses': [
                    user.email,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': email_format,
                    }
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': 'Código de verificação',
                }
            },
            Source=os.environ.get('SES_SENDER'),
        )

        return {'body': {'email': auth['email'],
                         'verification_email_code_expires_at': verification_email_code_expires_at}}
