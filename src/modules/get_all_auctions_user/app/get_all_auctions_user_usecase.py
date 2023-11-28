from typing import Dict, Optional, List

from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.errors.modules_errors import UserNotAuthenticated
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.interface.auction_interface import AuctionInterface
from src.shared.structure.enums.user_enum import TYPE_ACCOUNT_USER_ENUM, STATUS_USER_ACCOUNT_ENUM


class GetAllAuctionsUserUseCase:
    def __init__(self, auction_interface: AuctionInterface, user_interface: UserInterface):
        self.__token = TokenAuthy()
        self.__user_interface = user_interface
        self.__auction_interface = auction_interface

    def __call__(self, auth: Dict, body: Dict) -> Dict[str, List[Dict]]:
        if not auth.get('Authorization'):
            raise UserNotAuthenticated('Token de acesso não encontrado.')
        decoded_token = self.__token.decode_token(auth.get('Authorization'))
        if not decoded_token:
            raise UserNotAuthenticated("Token de acesso inválido ou expirado.")
        user_id = decoded_token.get('user_id')
        user = self.__user_interface.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotAuthenticated()
        if TYPE_ACCOUNT_USER_ENUM(user.get('type_account')) != TYPE_ACCOUNT_USER_ENUM.USER:
            raise UserNotAuthenticated()
        if STATUS_USER_ACCOUNT_ENUM(user.get('status_account')) != STATUS_USER_ACCOUNT_ENUM.ACTIVE:
            raise UserNotAuthenticated()

        return {
            "auctions": self.__auction_interface.get_all_auctions_user(user_id=user_id, status_auction=body.get('status_auction'))
        }
