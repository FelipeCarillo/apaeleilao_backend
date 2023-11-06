from typing import Dict, Optional

from src.shared.errors.modules_errors import *
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.entities.bid import Bid
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM
from src.shared.structure.interface.auction_interface import AuctionInterface


class GetBidUseCase:
    def __init__(self, user_interface: UserInterface, auction_interface: AuctionInterface):
        self.__user_interface = user_interface
        self.__auction_interface = auction_interface
        self.__token = TokenAuthy()

    def __call__(self, auth: Dict, body: Dict) -> Optional[Dict]:
        if not auth.get('Authorization'):
            raise UserNotAuthenticated('Token de acesso não encontrado.')

        decoded_token = self.__token.decode_token(auth["Authorization"])
        if not decoded_token:
            raise UserNotAuthenticated("Token de acesso inválido ou expirado.")
        user_id = decoded_token.get('user_id')
        user = self.__user_interface.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotAuthenticated()

        status_account_permitted = [STATUS_USER_ACCOUNT_ENUM.ACTIVE]
        if STATUS_USER_ACCOUNT_ENUM(user.get('status_account')) not in status_account_permitted:
            raise UserNotAuthenticated(message='Sua conta está suspensa.')

        bids = self.__auction_interface.get_all_bids_by_auction_id(auction_id=body.get('auction_id'))
        if not bids:
            raise InvalidParameter(parameter='Leilão', body='não encontrado')
        if len(bids) == 0:
            return None
        bids = [Bid(
            bid_id=bid.get('bid_id'),
            auction_id=bid.get('auction_id'),
            user_id=bid.get('user_id'),
            amount=bid.get('amount'),
            created_at=bid.get('created_at')
        ) for bid in bids]

        return [bid.to_dict() for bid in bids]
