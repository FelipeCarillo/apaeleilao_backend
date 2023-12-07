from typing import Dict

from src.shared.errors.modules_errors import *
from src.shared.structure.entities.auction import Auction
from src.shared.helper_functions.email_function import Email
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.helper_functions.events_trigger import EventsTrigger
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM
from src.shared.helper_functions.time_manipulation import TimeManipulation
from src.shared.structure.interface.auction_interface import AuctionInterface
from src.shared.structure.enums.user_enum import TYPE_ACCOUNT_USER_ENUM, STATUS_USER_ACCOUNT_ENUM


class DeleteAuctionUseCase:
    def __init__(self, auction_interface: AuctionInterface, user_interface: UserInterface):
        self.__email = Email()
        self.__token = TokenAuthy()
        self.__trigger = EventsTrigger()
        self.__user_interface = user_interface
        self.__auction_interface = auction_interface

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

        auction_id = body.get("auction_id")
        if not auction_id:
            raise MissingParameter('auction_id')
        
        auction = self.__auction_interface.get_auction_by_id(auction_id=auction_id)
        stutus_auction_not_authorized = [STATUS_AUCTION_ENUM.SUSPENDED.value,
                                         STATUS_AUCTION_ENUM.OPEN.value,
                                         STATUS_AUCTION_ENUM.CLOSED.value]
        if not auction or auction.get('status_auction') in stutus_auction_not_authorized:
            raise DataNotFound(f"Leilão - Lote[{auction_id}] não encontrado.")

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
            status_auction=STATUS_AUCTION_ENUM.SUSPENDED.value,
            created_at=int(auction['created_at'])
        )

        self.__auction_interface.update_auction(auction=auction)

        self.__trigger.delete_rule(rule_name=f"start_auction_{auction.auction_id}_before",  lambda_function="start_auction")
        self.__trigger.delete_rule(rule_name=f"start_auction_{auction.auction_id}", lambda_function="start_auction")

        emails = self.__user_interface.get_all_users_to_send_email()
        if emails:
            time_now = TimeManipulation.get_current_time()

            email_body = f"""
                <div class="TextsBox" style="display: flex; justify-content: center; align-items: center;">
                    <div style="border: 1px solid black; border-radius: 10px; padding-bottom: 16px;">
                        <img style="border-radius: 10px 10px 0 0;" width="250" src="{auction.images[0]['image_body']}" alt="Imagem do {auction.title}">
                        <div style="color: #949393; text-align: center; margin-bottom: 16px;">
                            <h2 style="color:#000000;">{auction.title}</h2>
                            <p style="color:#000000">
                                Data: {TimeManipulation(time_now).get_datetime(datetime_format='%d-%m-%Y - %H:%M')}
                            </p>
                            <label style="color: red; font-weight: bold; font-size: 24px;">Suspenso</label>
                        </div>
                    </div>
                </div>
                """
            self.__email.set_email_template(f"Leilão {auction.title} - LOTE[{auction_id}] cancelado.", email_body)

            self.__email.send_email(to=emails,
                                    subject=f"Leilão {auction.title} cancelado.")
       
        return None
