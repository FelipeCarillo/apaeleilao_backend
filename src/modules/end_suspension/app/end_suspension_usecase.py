from typing import Dict
from datetime import datetime

from src.shared.errors.modules_errors import *
from src.shared.helper_functions.email_function import Email
from src.shared.helper_functions.events_trigger import EventsTrigger
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.suspension_enum import STATUS_SUSPENSION_ENUM
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM


class EndSuspensionUseCase:

    def __init__(self, user_interface: UserInterface):
        self.__email = Email()
        self.__trigger = EventsTrigger()
        self.__user_interface = user_interface

    def __call__(self, body: Dict):

        if not body:
            raise MissingParameter('body')

        suspension_id = body.get('suspension_id')
        if not suspension_id:
            raise MissingParameter('suspension_id')
        
        suspension = self.__user_interface.get_suspension_by_id(suspension_id=suspension_id)
        if not suspension:
            raise DataNotFound('Suspensão')

        if suspension.get("status_suspension") != STATUS_SUSPENSION_ENUM.ACTIVE.value:
            raise InvalidParameter('Suspensão', 'não está ativa')

        user_id = suspension.get('user_id')
        user = self.__user_interface.get_user_by_id(user_id=user_id)

        self.__user_interface.update_suspension_status(user_id=suspension.get("user_id"), status=STATUS_SUSPENSION_ENUM.ENDED.value)

        self.__user_interface.update_user_status(user_id=suspension.get('user_id'), status=STATUS_USER_ACCOUNT_ENUM.ACTIVE.value)

        self.__trigger.delete_rule(rule_name=f"end_suspension_{suspension.get('suspension_id')}",  lambda_function="end_suspension")

        date_suspension = datetime.fromtimestamp(suspension.get("date_suspension")).strftime('%d/%m/%Y %H:%M:%S')
        date_reactivation = datetime.fromtimestamp(suspension.get("date_reactivation")).strftime('%d/%m/%Y %H:%M:%S')

        email_body = f"""
            <h1>Suspensão<span style="font-weight: bold;"></span> Finalizada!</h1>
            <p>Sua suspensão foi cumprida.</p>
            <p>Data de início: {date_suspension}</p>
            <p>Data de término: {date_reactivation}</p>
            <p>Motivo da suspensão: {suspension.get("reason")}</p>
            <p>Para mais informações acesse o site.</p>
            """

        self.__email.set_email_template(f"Suspensão cumprida", email_body)
        self.__email.send_email(
            to=user.get('email'),
            subject='Suspensão finalizada')

        return None
    