from typing import Dict

from src.shared.errors.modules_errors import *
from src.shared.structure.entities.auction import Auction
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM
from src.shared.structure.interface.auction_interface import AuctionInterface


class GetAuctionUseCase:
    def __init__(self, user_interface: UserInterface, auction_interface: AuctionInterface):
        self.__user_interface = user_interface
        self.__auction_interface = auction_interface
        self.__token = TokenAuthy()

    def __call__(self, auth: Dict, body: Dict) -> Dict:
        if not auth.get('Authorization'):
            raise MissingParameter('Authorization')

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

        if not body.get('auction_id'):
            raise MissingParameter('auction_id')
        auction = self.__auction_interface.get_auction_by_id(auction_id=body.get('auction_id'))
        if not auction:
            raise DataNotFound('Leilão')

        if auction.get('status_auction') != STATUS_USER_ACCOUNT_ENUM:
            raise DataNotFound('Leilão')

        auction = Auction(
            auction_id=auction.get('auction_id'),
            created_by=auction.get('created_by'),
            tittle=auction.get('tittle'),
            description=auction.get('description'),
            start_date=auction.get('start_date'),
            end_date=auction.get('end_date'),
            start_amount=auction.get('start_amount'),
            current_amount=auction.get('current_amount'),
            images=auction.get('images'),
            status_auction=auction.get('status_auction'),
            create_at=auction.get('create_at')
        )
        auction.check_time()

        if auction.status_auction.value != body.get('status_auction'):
            self.__auction_interface.update_auction_bids(auction=auction)

        return auction.to_dict()