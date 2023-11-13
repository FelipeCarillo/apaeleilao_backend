from typing import Dict

from src.shared.errors.modules_errors import *
from src.shared.structure.enums.user_enum import *
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.helper_functions.mercadopago_api import MercadoPago
from src.shared.helper_functions.events_trigger import EventsTrigger
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.interface.auction_interface import AuctionInterface


class GetPaymentUseCase:

    def __init__(self, auction_interface: AuctionInterface, user_interface: UserInterface):
        self.__token = TokenAuthy()
        self.__payment = MercadoPago()
        self.__trigger = EventsTrigger()
        self.__user_interface = user_interface
        self.__auction_interface = auction_interface

    def __call__(self, auth: Dict, body: Dict) -> Dict:

        if not auth.get('Authorization'):
            raise UserNotAuthenticated("token de acesso não encontrado.")
        
        decoded_token = self.__token.decode_token(body["Authorization"])
        if not decoded_token:
            raise UserNotAuthenticated("Token de acesso inválido ou expirado.")
        
        user_id = decoded_token.get('user_id')
        user = self.__user_interface.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotAuthenticated()

        if not body:
            MissingParameter('body')

        if not body.get("auction_id"):
            raise MissingParameter("auction_id")
        
        payment = self.__auction_interface.get_payment_by_auction(auction_id=body.get('auction_id'))
        if not payment:
            raise DataNotFound('Pagamento')
        payment_mercadopago = self.__payment.get_payment(payment_id=payment.get('payment_id'))
        if not payment_mercadopago:
            raise DataNotFound('Pagamento')

        accounts_permitted = [TYPE_ACCOUNT_USER_ENUM.ADMIN, TYPE_ACCOUNT_USER_ENUM.MODERATOR]
        if STATUS_USER_ACCOUNT_ENUM(user.get('status_account')) != STATUS_USER_ACCOUNT_ENUM.ACTIVE:
            raise UserNotAuthenticated("Sua conta está suspensa.")
        
        if TYPE_ACCOUNT_USER_ENUM(user.get("type_account")) not in accounts_permitted:
            if payment.get("user_id") != user_id:
                raise UserNotAuthenticated("Pagamento não pertence ao usuário.")
        else:
            raise UserNotAuthenticated("Você não tem permissão para acessar este recurso.")
        
        return payment
