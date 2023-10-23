from typing import Dict

from src.shared.structure.entities.bid import Bid
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import TYPE_ACCOUNT_USER_ENUM
from src.shared.helper_functions.time_manipulation import TimeManipulation
from src.shared.structure.interface.auction_interface import AuctionInterface
from src.shared.errors.modules_errors import MissingParameter, UserNotAuthenticated, DataNotFound


class CreateUserUseCase:
    def __init__(self, user_interface: UserInterface, auction_interface: AuctionInterface):
        self.__user_interface = user_interface
        self.__auction_interface = auction_interface
        self.__token = TokenAuthy()

    def __call__(self, auth: Dict, body: Dict) -> None:

        if not auth.get('Authorization'):
            raise MissingParameter('Authorization')

        decoded_token = self.__token.decode_token(auth.get('Authorization'))
        if not decoded_token:
            raise UserNotAuthenticated("Token de acesso inválido ou expirado.")
        user_id = decoded_token.get('user_id')
        user = self.__user_interface.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotAuthenticated()
        AUTHORIZED_TYPE_ACCOUNT = [TYPE_ACCOUNT_USER_ENUM.USER]
        if TYPE_ACCOUNT_USER_ENUM(user.get('type_account')) not in AUTHORIZED_TYPE_ACCOUNT:
            raise UserNotAuthenticated()

        if not body.get('auction_id'):
            raise MissingParameter('auction_id')

        if not body.get('amount'):
            raise MissingParameter('amount')

        if self.__auction_interface.get_auction_by_id(auction_id=body.get('auction_id')):
            raise DataNotFound('Leilão')

        last_bid_id = self.__auction_interface.get_last_bid_id()
        bid_id = last_bid_id + 1 if last_bid_id else 1

        bid = Bid(
            bid_id=str(bid_id),
            user_id=user.get('user_id'),
            auction_id=body.get('auction_id'),
            amount=body.get('amount'),
            create_at=TimeManipulation().get_current_time()
        )
        self.__auction_interface.create_bid(bid=bid)

        bids = self.__auction_interface.get_bids_by_auction(auction_id=body.get('auction_id'), limit=1)
        if bids:
            auction = {"auction_id": body.get('auction_id'), "current_amount": bids[0].get('amount')}
            self.__auction_interface.update_auction_information(auction_dict=auction)

        return None
