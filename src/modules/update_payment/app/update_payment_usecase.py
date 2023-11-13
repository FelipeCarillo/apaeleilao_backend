from typing import Dict

from src.shared.errors.modules_errors import *
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.helper_functions.mercadopago_api import MercadoPago
from src.shared.structure.interface.auction_interface import AuctionInterface
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_PAYMENT_ENUM


class UpdatePaymentUseCase:

    def __init__(self, auction_interface: AuctionInterface):
        self.__token = TokenAuthy()
        self.__payment = MercadoPago()
        self.__auction_interface = auction_interface

    def __call__(self, auth: Dict, body: Dict):

        # if not auth.get("referer"):
        #     raise UserNotAuthenticated("não encontrado.")

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

        return self.__auction_interface.update_status_payment(auction_id=payment.get('auction_id'),
                                                              payment_id=payment.get('payment_id'),
                                                              status_payment=payment.get('status_payment'))
