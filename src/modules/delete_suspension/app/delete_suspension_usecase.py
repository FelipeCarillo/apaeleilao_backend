from typing import Dict

from src.shared.errors.modules_errors import *
from src.shared.helper_functions.email_function import Email
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.helper_functions.events_trigger import EventsTrigger
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.suspension_enum import STATUS_SUSPENSION_ENUM
from src.shared.structure.enums.user_enum import TYPE_ACCOUNT_USER_ENUM, STATUS_USER_ACCOUNT_ENUM
from src.shared.structure.entities.suspension import Suspension
from src.shared.structure.enums.suspension_enum import STATUS_SUSPENSION_ENUM


class DeleteSuspensionUseCase:

    def __init__(self, user_interface: UserInterface):
        self.__email = Email()
        self.__token = TokenAuthy()
        self.__trigger = EventsTrigger()
        self.__user_interface = user_interface

    def __call__(self, auth: Dict, body: Dict) -> None:

        if not auth.get('Authorization'):
            raise UserNotAuthenticated('Token de acesso não encontrado.')
        if not body:
            raise MissingParameter('body')
        
        decoded_token = self.__token.decode_token(auth.get('Authorization'))
        if not decoded_token:
            raise UserNotAuthenticated("Token de acesso inválido ou expirado.")
        
        user_id = decoded_token.get('user_id')
        user = self.__user_interface.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotAuthenticated()
        
        AUTHORIZED_TYPE_ACCOUNT = [TYPE_ACCOUNT_USER_ENUM.ADMIN, TYPE_ACCOUNT_USER_ENUM.MODERATOR]
        if TYPE_ACCOUNT_USER_ENUM(user.get('type_account')) not in AUTHORIZED_TYPE_ACCOUNT:
            raise UserNotAuthenticated()
        if STATUS_USER_ACCOUNT_ENUM(user.get('status_account')) != STATUS_USER_ACCOUNT_ENUM.ACTIVE:
            raise UserNotAuthenticated()
        
        suspension_id = body.get("suspension_id")
        if not suspension_id:
            raise MissingParameter('suspension_id')
        
        suspension = self.__user_interface.get_suspension_by_id(suspension_id=suspension_id)
        if not suspension:
            raise DataNotFound(f"Suspensão")
        
        if suspension.get("status_suspension") != STATUS_SUSPENSION_ENUM.ACTIVE.value:
            raise InvalidParameter(f"Suspensão", "não está ativa")
 
        self.__user_interface.update_suspension_status(user_id=suspension.get('user_id'), status=STATUS_SUSPENSION_ENUM.CANCEL)

        self.__user_interface.update_user_status(user_id=suspension.get('user_id'), status=STATUS_USER_ACCOUNT_ENUM.ACTIVE)

        self.__trigger.delete_rule(rule_name=f"end_suspension_{suspension.get('user_id')}",  lambda_function="end_suspension")

        email_body = f"""
            <h1>Suspensão<span style="font-weight: bold;"></span> Finalizada!</h1>
            <p>Sua suspensão foi cumprida.</p>
            <p>Data de início: {suspension.get("date_suspension")}</p>
            <p>Data de término: {suspension.get("date_reactivation")}</p>
            <p>Motivo da suspensão: {suspension.get("reason")}</p>
            <p>Para mais informações acesse o site.</p>
            """
                
        self.__email.set_email_template(f"Suspensão cumprida", email_body)
        self.__email.send_email(
            to=suspension.get('email'),
            subject='Suspensão finalizada')
        
        return None
