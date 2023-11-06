import os
import smtplib
from typing import Sequence
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


default_footer = """
    <div class="TextsBox" style="color: #949393; word-wrap: break-word;">'
      <h2>Atenciosamente,</h2>
      <h2>
        <b>IMT</b>
      </h2>
    </div>
"""


class Email:
    def __init__(self):
        self.email_body = None
        self.__email = os.environ.get('EMAIL_SENDER')
        self.__password = os.environ.get('EMAIL_PASSWORD')
        self.__host = os.environ.get('EMAIL_HOST')
        self.__port = int(os.environ.get('EMAIL_PORT'))

    def __connect(self):
        self.__server = smtplib.SMTP(self.__host, self.__port)
        self.__server.starttls()
        self.__server.login(self.__email, self.__password)

    def __disconnect(self):
        self.__server.quit()

    def send_email(self, to, subject: str):
        try:
            message = MIMEMultipart()
            message['From'] = self.__email
            message['To'] = to
            message['Subject'] = subject
            message.attach(MIMEText(self.__email, 'html'))
            self.__connect()
            self.__server.sendmail(self.__email, to, message.as_string())
            self.__disconnect()
        except Exception as e:
            if self.__server:
                self.__disconnect()
            raise e

    def set_email_template(self, title, content: str,
                           footer: str = default_footer):
        self.email_body = f"""
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
                                    <h1 style="color: #FFFFFF; margin-top: 10px;"><b>{title}</b></h1>
                                </td>
                            </tr>
                        </table>
                        <table class="ContentBox" style="width: 100%; background-color: #FFFFFF;">
                            <tr>
                                <td style="text-align: center; padding: 20px;">
                                    {content}
                                </td>
                            </tr>
                        </table>
                        <table class="BottomBox"
                            style="width: 100%; background-color: #FFFFFF; border-top: 1px solid gray; border-radius: 0 0 10px 10px;">
                            <tr>
                                <td style="text-align: center; padding: 20px;">
                                    {footer}
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
