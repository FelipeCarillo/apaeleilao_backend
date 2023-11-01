from typing import Dict

from src.shared.errors.modules_errors import *
from src.shared.structure.entities.auction import Auction
from src.shared.helper_functions.email_function import Email
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM
from src.shared.structure.interface.auction_interface import AuctionInterface


class EndAuctionUseCase:

    def __init__(self, auction_interface: AuctionInterface):
        self.__auction_interface = auction_interface
        self.__token = TokenAuthy()
        self.__email = Email()

    def __call__(self, body: Dict):

        if not body:
            MissingParameter('body')

        auction_id = body.get('auction_id')
        if not auction_id:
            raise MissingParameter('auction_id')

        auction = self.__auction_interface.get_auction_by_id(auction_id=auction_id)
        if not auction:
            raise DataNotFound('Leilão')

        auction = Auction(
            auction_id=auction["auction_id"],
            created_by=auction["user_id"],
            title=auction["title"],
            description=auction["description"],
            start_date=auction["start_date"],
            end_date=auction["end_date"],
            start_amount=auction["start_amount"],
            current_amount=auction["current_amount"],
            status_auction=auction["status_auction"],
            created_at=auction["created_at"],
        )

        auction.status_auction = STATUS_AUCTION_ENUM.CLOSED

        self.__auction_interface.update_auction(auction)
        bids = self.__auction_interface.get_all_bids_by_auction_id(auction_id=auction_id)
        if bids:
            email_body = f"""
            """

            self.__email.send_email(,
                                    "Leilão encerrado",
                                    email_body)






