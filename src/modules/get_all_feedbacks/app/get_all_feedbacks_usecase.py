from typing import Dict

from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.errors.modules_errors import UserNotAuthenticated
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import TYPE_ACCOUNT_USER_ENUM, STATUS_USER_ACCOUNT_ENUM


class GetAllFeedbacksUseCase:
    def __init__(self, user_interface: UserInterface):
        self.__token = TokenAuthy()
        self.__user_interface = user_interface

    def __call__(self, auth: Dict):
        if not auth.get('Authorization'):
            raise UserNotAuthenticated('Token de acesso não encontrado.')
        decoded_token = self.__token.decode_token(auth.get('Authorization'))
        if not decoded_token:
            raise UserNotAuthenticated("Token de acesso inválido ou expirado.")
        user_id = decoded_token.get('user_id')
        user = self.__user_interface.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotAuthenticated()
        if TYPE_ACCOUNT_USER_ENUM(user.get('type_account')) not in [TYPE_ACCOUNT_USER_ENUM.ADMIN, TYPE_ACCOUNT_USER_ENUM.MODERATOR]:
            raise UserNotAuthenticated()
        if STATUS_USER_ACCOUNT_ENUM(user.get('status_account')) != STATUS_USER_ACCOUNT_ENUM.ACTIVE:
            raise UserNotAuthenticated()

        feedbacks = self.__user_interface.get_all_feedbacks()

        response = {
            "feedbacks": feedbacks,
            "total_feedbacks": len(feedbacks) if feedbacks else "Sem avaliações",
            "mean_feedback": sum([feedback.get('grade') for feedback in feedbacks]) / len(feedbacks) if feedbacks else "Sem avaliações",
        }

        return response
