import os
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
        self.__domain = os.environ.get('DOMAIN')
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

        emails = self.__user_interface.get_all_users_to_send_email()
        auction_start_date = TimeManipulation(auction.start_date).plus_hour(-3)

        time_now = body.get("time_now", None)
        if time_now:
            if emails:
                minutes_before = int((auction.start_date - time_now) / 60)

                email_body = f"""
                <div class="TextsBox" style="display: flex; justify-content: center; align-items: center;">
                    <div style="border: 1px solid black; border-radius: 10px; padding-bottom: 16px;">
                        <img style="border-radius: 10px 10px 0 0;" width="250" src="http://via.placeholder.com/500x500" alt="">
                        <div style="color: #949393; text-align: center; margin-bottom: 16px;">
                            <h2 style="color:#000000;">{auction.title}</h2>
                            <p style="color:#000000">Data: {TimeManipulation(auction_start_date).get_datetime(datetime_format='%d-%m-%Y - %H:%M')}</p>
                            <label style="color: black; font-weight: bold; font-size: 24px;">Lance: R${auction.current_amount}</label>
                        </div>
                        <a style="background-color: yellow; border: none; padding: 6px 12px; font-size: 16px; font-weight: bold; border-radius: 25px; margin: 8px; color: black;" href="https://{self.__domain}"> Ir para o Leilão </a>
                    </div>
                </div>
                """
                self.__email.set_email_template(f"Leilão {auction.title} - LOTE[{auction_id}] iniciará em {minutes_before} minuto{'s' if minutes_before > 1 else ''}!",
                                                email_body)
                self.__email.send_email(to=emails,
                                        subject=f"Leilão iniciará em {minutes_before} minuto{'s' if minutes_before > 1 else ''}!")

            self.__trigger.delete_rule(rule_name=f"start_auction_{auction.auction_id}_before",
                                       lambda_function=f"start_auction")

        else:
            self.__auction_interface.update_auction(auction)
            if emails:
                email_body = f"""
                <div class="TextsBox" style="display: flex; justify-content: center; align-items: center;">
                    <div style="border: 1px solid black; border-radius: 10px; padding-bottom: 16px;">
                        <img style="border-radius: 10px 10px 0 0;" width="250" src="http://via.placeholder.com/500x500" alt="">
                        <div style="color: #949393; text-align: center; margin-bottom: 16px;">
                            <h2 style="color:#000000;">{auction.title}</h2>
                            <p style="color:#000000">Data: {TimeManipulation(auction_start_date).get_datetime(datetime_format='%d-%m-%Y - %H:%M')}</p>
                            <label style="color: black; font-weight: bold; font-size: 24px;">Lance: R${auction.current_amount}</label>
                        </div>
                        <a style="background-color: yellow; border: none; padding: 6px 12px; font-size: 16px; font-weight: bold; border-radius: 25px; margin: 8px; color: black;" href="https://{self.__domain}"> Ir para o Leilão </a>
                    </div>
                </div>
                """
                self.__email.set_email_template(f"Leilão {auction.title} - LOTE[{auction_id}] começou!",
                                                email_body)
                self.__email.send_email(to=emails,
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
