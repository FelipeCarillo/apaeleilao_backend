from uuid import uuid4
from typing import Dict

from src.shared.errors.modules_errors import *
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.entities.suspension import Suspension
from src.shared.helper_functions.mercadopago_api import MercadoPago
from src.shared.helper_functions.events_trigger import EventsTrigger
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM
from src.shared.helper_functions.time_manipulation import TimeManipulation
from src.shared.structure.interface.auction_interface import AuctionInterface
from src.shared.structure.enums.suspension_enum import STATUS_SUSPENSION_ENUM
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_PAYMENT_ENUM


class UpdatePaymentWebhookUseCase:

    def __init__(self, auction_interface: AuctionInterface, user_interface: UserInterface):
        self.__token = TokenAuthy()
        self.__payment = MercadoPago()
        self.__trigger = EventsTrigger()
        self.__user_interface = user_interface
        self.__auction_interface = auction_interface

    def __call__(self, auth: Dict, body: Dict):

        if not body:
            raise MissingParameter('body')

        if body.get("action") != "payment.updated":
            return None

        payment = self.__auction_interface.get_payment_by_id(payment_id=body.get('data').get('id'))
        if not payment:
            raise DataNotFound('Pagamento')

        service_payment = self.__payment.get_payment(payment_id=payment.get('payment_id'))
        if not service_payment:
            raise DataNotFound('Pagamento')

        if service_payment.get('status') == "approved":
            payment['status_payment'] = STATUS_AUCTION_PAYMENT_ENUM.PAID

        if service_payment.get('status') == "cancelled":
            payment['status_payment'] = STATUS_AUCTION_PAYMENT_ENUM.EXPIRED

            suspensions = self.__user_interface.get_all_suspensions_by_user_id(user_id=payment.get('user_id'))
            suspensions_length = len(suspensions)
            if suspensions_length == 0:
                date_reactivation = TimeManipulation().plus_day(days=7)
            elif suspensions_length == 1:
                date_reactivation = TimeManipulation().plus_day(days=14)
            else:
                date_reactivation = None

            auction = self.__auction_interface.get_auction_by_id(auction_id=payment.get('auction_id'))
            suspension = Suspension(
                user_id=payment.get('user_id'),
                suspension_id=uuid4().hex,
                reason=f"Pagamento do Leilão {auction.get('title')} - Lote[{auction.get('auction_id')}] não foi "
                       f"efetuado no prazo de 5 dias.",
                created_at=TimeManipulation.get_current_time(),
                status_suspension=STATUS_SUSPENSION_ENUM.ACTIVE,
                date_suspension=TimeManipulation.get_current_time(),
                date_reactivation=date_reactivation
            )
            self.__user_interface.create_suspension(suspension=suspension)
            if suspensions_length != 2:
                self.__user_interface.update_user_status(user_id=payment.get('user_id'),
                                                         status=STATUS_USER_ACCOUNT_ENUM.SUSPENDED)
                payload = {
                    "body": {
                        "suspension_id": suspension.suspension_id,
                    }
                }
                self.__trigger.create_trigger(f"end_suspension_{suspension.suspension_id}", "end_suspension",
                                              suspension.date_reactivation, payload)
            else:
                self.__user_interface.update_user_status(user_id=payment.get('user_id'),
                                                         status=STATUS_USER_ACCOUNT_ENUM.BANED)

        return self.__auction_interface.update_status_payment(auction_id=payment.get('auction_id'),
                                                              payment_id=payment.get('payment_id'),
                                                              status_payment=payment.get('status_payment'))
