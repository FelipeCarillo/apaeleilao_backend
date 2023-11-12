import os
import mercadopago

from src.shared.structure.entities.payment import Payment
from src.shared.helper_functions.time_manipulation import TimeManipulation


class MercadoPago:
    def __init__(self):
        self.__payment_preference = None
        self.__access_token = os.environ.get('MERCADO_PAGO_ACCESS_TOKEN')
        self.__mp = mercadopago.SDK(self.__access_token)

    def create_payment(self):
        payment = self.__mp.payment().create(self.__payment_preference)
        if payment['status'] == 201:
            return payment['response']
        else:
            raise Exception(payment['response'])

    def get_payment(self, payment_id):
        payment = self.__mp.payment().get(payment_id)
        if payment['status'] == 200:
            return payment['response']
        else:
            raise Exception(payment['response'])

    def set_payment_preference(self, payment: Payment):
        time = TimeManipulation()
        time.plus_hour(-1)
        time.plus_day(5)
        date_of_expiration = time.get_datetime(datetime_format="%Y-%m-%dT%H:%M:%S.000-04:00")

        self.__payment_preference = {
            "additional_info": {
                "items": [
                    {
                        "id": payment.auction_id,
                        "title": payment.auction_title,
                        "description": payment.auction_description,
                        "quantity": 1,
                        "unit_price": payment.amount,
                    }
                ]
            },
            "payer": {
                "email": "carillofelipe345@gmail.com",
                "first_name": payment.first_name,
                "last_name": payment.last_name,
                "identification": {
                    "type": "CPF",
                    "number": payment.cpf,
                },
                "phone": {
                    "area_code": "+55",
                    "number": payment.phone,
                },
            },
            "payment_method_id": "pix",
            "transaction_amount": payment.amount,
            "date_of_expiration": date_of_expiration,
        }
