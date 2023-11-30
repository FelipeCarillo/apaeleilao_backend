from typing import Dict

from src.shared.errors.modules_errors import *
from src.shared.structure.entities.suspension import Suspension
from src.shared.helper_functions.email_function import Email
from src.shared.helper_functions.time_manipulation import TimeManipulation
from src.shared.structure.interface.suspension_interface import SuspensionInterface
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.suspension_enum import STATUS_SUSPENSION_ENUM
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM


class EndSuspensionUseCase:

    def __init__(self, suspension_interface: SuspensionInterface, user_interface: UserInterface):
        self.__email = Email()
        self.__suspension_interface = suspension_interface
        self.__user_interface = user_interface

    def __call__(self, body: Dict):

        if not body:
            raise MissingParameter('body')

        suspension_id = body.get('suspension_id')
        if not suspension_id:
            raise MissingParameter('suspension_id', 'não encontrado')
        
        suspension = self.__suspension_interface.get_suspension_by_id(suspension_id=suspension_id)
        if not suspension:
            raise DataNotFound('Suspensão')
        
        suspension = Suspension(
            user_id=suspension['user_id'],
            suspension_id=suspension['suspension_id'],
            date_suspension=int(suspension['date_suspension']),
            date_reactivation=int(suspension['date_reactivation']),
            reason=suspension['reason'],
            created_at=int(suspension['created_at']),
        )
        suspension_status = self.__suspension_interface.get_suspension_by_id(suspension_id=suspension_id)

        if suspension_status == STATUS_SUSPENSION_ENUM.ACTIVE.value:

            if suspension.date_reactivation == TimeManipulation.get_current_time():

                self.__user_interface.update_suspension_status(user_id=suspension.user_id, status_suspension=STATUS_SUSPENSION_ENUM.ENDED.value)

                self.__user_interface.update_user_status(user_id=suspension.get('user_id'), status_account=STATUS_USER_ACCOUNT_ENUM.ACTIVE.value)

                email_body = f"""
            <h1>Suspensão<span style="font-weight: bold;"></span> Finalizada!</h1>
            <p>Sua suspensão foi cumprida.</p>
            <p>Data de início: {suspension.date_suspension}</p>
            <p>Data de término: {suspension.date_reactivation}</p>
            <p>Motivo da suspensão: {suspension.reason}</p>
            <p>Para mais informações acesse o site.</p>
            """
                
                self.__email.set_email_template(f"Suspensão cumprida", email_body)
                self.__email.send_email(
                    to=suspension.user_id.get('email'),
                    subject='Suspensão finalizada')
        
        return None
        