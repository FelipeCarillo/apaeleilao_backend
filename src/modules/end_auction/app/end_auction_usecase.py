from typing import Dict

from src.shared.errors.modules_errors import *
from src.shared.structure.entities.auction import Auction
from src.shared.structure.entities.payment import Payment
from src.shared.helper_functions.email_function import Email
from src.shared.helper_functions.mercadopago_api import MercadoPago
from src.shared.helper_functions.events_trigger import EventsTrigger
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.helper_functions.time_manipulation import TimeManipulation
from src.shared.structure.interface.auction_interface import AuctionInterface
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM, PAYMENT_SERVICES, STATUS_AUCTION_PAYMENT_ENUM


class EndAuctionUseCase:

    def __init__(self, auction_interface: AuctionInterface, user_interface: UserInterface):
        self.__email = Email()
        self.__payment = MercadoPago()
        self.__trigger = EventsTrigger()
        self.__user_interface = user_interface
        self.__auction_interface = auction_interface

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
            created_by=auction["created_by"],
            images=auction["images"],
            title=auction["title"],
            description=auction["description"],
            start_date=int(auction["start_date"]),
            end_date=int(auction["end_date"]),
            start_amount=auction["start_amount"],
            current_amount=auction["current_amount"],
            status_auction=auction["status_auction"],
            created_at=int(auction["created_at"]),
        )
        bids = self.__auction_interface.get_all_bids_by_auction_id(auction_id=auction_id)

        if not bids:
            auction.status_auction = STATUS_AUCTION_ENUM.AVAILABLE
            self.__auction_interface.update_auction(auction)

        else:
            auction.status_auction = STATUS_AUCTION_ENUM.CLOSED

            self.__auction_interface.update_auction(auction)
            bids_sorted = sorted(bids, key=lambda k: k['amount'], reverse=True)

            winner = bids_sorted[0]
            winner_email = winner.get('email')
            to_emails = list(set([item.get('email') for item in bids_sorted][1:]))

            email_body = f"""
            <h1>Leilão<span style="font-weight: bold;">{auction.title} LOTE[{auction.auction_id}]</span> Finalizado!</h1>
            <p>Parabéns você ganhou o leilão!</p>
            <p>Para mais informações acesse o site.</p>
            """
            self.__email.set_email_template(f"Leilão {auction.title} Finalizado", email_body)
            self.__email.send_email(to=winner_email, subject='Você Ganhou o Leilão')

            if len(to_emails) > 0:
                email_body = f"""
                            <h1>Leilão<span style="font-weight: bold;">LOTE[{auction.auction_id}]</span> Finalizado!</h1>
                            <p>Infelizmente você não ganhou o leilão.</p>
                            <p>Para mais informações acesse o site.</p>
                            """
                self.__email.set_email_template(f"Leilão {auction.title} Finalizado", email_body)
                self.__email.send_email(to=to_emails, subject='Leilão encerrado')

            self.__trigger.delete_rule(rule_name=f"end_auction_{auction_id}", lambda_function=f"End_Auction")

            user = self.__user_interface.get_user_by_email(email=winner_email)

            payment = Payment(
                auction_id=auction.auction_id,
                user_id=user.get('user_id'),
                auction_title=auction.title,
                auction_description=auction.description,
                first_name=user.get('first_name'),
                last_name=user.get('last_name'),
                cpf=user.get('cpf'),
                phone=user.get('phone'),
                email=user.get('email'),
                amount=winner.get('amount'),
                created_at=TimeManipulation.get_current_time(),
                status_payment=STATUS_AUCTION_PAYMENT_ENUM.PENDING,
                payment_service=PAYMENT_SERVICES.MERCADO_PAGO
            )

            self.__payment.set_payment_preference(payment=payment)
            payment_created = self.__payment.create_payment()

            payment.payment_id = str(payment_created.get('id'))
            date_of_expiration = payment_created.get('date_of_expiration').replace('T', ' ').replace('.000-04:00', '')
            date_of_expiration = TimeManipulation(datetime_now=date_of_expiration).get_time()
            payment.payment_expires_at = date_of_expiration
            self.__auction_interface.create_payment(payment=payment)

        return None
