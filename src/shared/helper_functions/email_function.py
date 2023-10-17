import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self):
        self.__email = os.environ.get('EMAIL_SENDER')
        self.__password = os.environ.get('EMAIL_PASSWORD')
        self.__host = os.environ.get('EMAIL_HOST')
        self.__port = int(os.environ.get('EMAIL_PORT'))
        self.__server = smtplib.SMTP(self.__host, self.__port)

    def send_email(self, to: str, subject: str, body: str):
        try:
            message = MIMEMultipart()
            message['From'] = self.__email
            message['To'] = to
            message['Subject'] = subject
            message.attach(MIMEText(body, 'html'))
            self.__server.starttls()
            self.__server.login(self.__email, self.__password)
            self.__server.sendmail(self.__email, to, message.as_string())
            self.__server.quit()
        except Exception as e:
            raise e
