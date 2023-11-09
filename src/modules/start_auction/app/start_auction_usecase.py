from typing import Any, Dict

from src.shared.errors.modules_errors import *
from src.shared.helper_functions.email_function import Email
from src.shared.helper_functions.events_trigger import EventsTrigger
from src.shared.helper_functions.time_manipulation import TimeManipulation
from src.shared.structure.entities.auction import Auction
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.interface.auction_interface import AuctionInterface


class StartAuctionUseCase:

    def __init__(self, auction_interface: AuctionInterface, user_interface: UserInterface):
        self.__email = Email()
        self.__trigger = EventsTrigger()
        self.__user_interface = user_interface
        self.__auction_interface = auction_interface

    def __call__(self, body: Dict) -> Any:

        if not body:
            raise MissingParameter('body')

        auction_id = body.get("auction_id")
        if not auction_id:
            raise MissingParameter('auction_id')

        auction = self.__auction_interface.get_auction_by_id(auction_id=auction_id)
        if not auction:
            raise DataNotFound('Leilão')

        auction = Auction(
            auction_id=auction_id,
            created_by=auction['created_by'],
            title=auction['title'],
            description=auction['description'],
            start_date=int(auction['start_date']),
            end_date=int(auction['end_date']),
            start_amount=float(auction['start_amount']),
            current_amount=float(auction['current_amount']),
            images=auction['images'] if auction['images'] else [],
            status_auction=STATUS_AUCTION_ENUM.OPEN.value,
            created_at=int(auction['created_at'])
        )

        users = self.__user_interface.get_all_users_to_send_email()
        if not users:
            to_email = []
        else:
            to_email = [email for email in users]

        time_now = body.get("time_now", None)
        if time_now:

            minutes_before = int((auction.start_date - time_now) / 60)

            email_body = f"""
            <h1>Leilão<span style="font-weight: bold;">{auction.title} LOTE[{auction.auction_id}]</span> Iniciará em {minutes_before} minuto{'s' if minutes_before > 1 else ''}!</h1><p>O leilão está prestes a começar.</p>
            <p>Para mais informações acesse o site.</p>
            """
            self.__email.set_email_template(f"Leilão {auction.title} Iniciará em {minutes_before} minuto{'s' if minutes_before > 1 else ''}!",
                                            email_body)
            self.__email.send_email(to=to_email,
                                    subject=f"Leilão iniciará em {minutes_before} minuto{'s' if minutes_before > 1 else ''}!")

            self.__trigger.delete_rule(rule_name=f"start_auction_{auction.auction_id}_before",
                                       lambda_function=f"start_auction")

        else:
            self.__auction_interface.update_auction(auction)

            email_body = f"""
            <h1>Leilão<span style="font-weight: bold;">{auction.title} LOTE[{auction.auction_id}]</span> Começou!</h1><p>O leilão está aberto.</p>
            <p>Para mais informações acesse o site.</p>
            """
            self.__email.set_email_template(f"Leilão {auction.title} Começou!",
                                            email_body)
            self.__email.send_email(to=to_email,
                                    subject="Leilão começou!")

            self.__trigger.delete_rule(rule_name=f"start_auction_{auction.auction_id}",
                                       lambda_function=f"start_auction")

            payload = {
                "body": {
                    "auction_id": auction.auction_id
                }
            }
            self.__trigger.create_trigger(rule_name=f"end_auction_{auction.auction_id}", lambda_function=f"end_auction",
                                          payload=payload, date=int(auction.end_date))
