from typing import Dict

from src.shared.structure.entities.auction import Auction
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.helper_functions.events_trigger import EventsTrigger
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.helper_functions.time_manipulation import TimeManipulation
from src.shared.helper_functions.image_manipulation import ImageManipulation
from src.shared.structure.interface.auction_interface import AuctionInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM, TYPE_ACCOUNT_USER_ENUM
from src.shared.errors.modules_errors import DataAlreadyUsed, MissingParameter, UserNotAuthenticated, InvalidParameter


class CreateUserUseCase:
    def __init__(self, user_interface: UserInterface, auction_interface: AuctionInterface):
        self.__token = TokenAuthy()
        self.__trigger = EventsTrigger()
        self.__user_interface = user_interface
        self.__auction_interface = auction_interface
        self.__image_manipulation = ImageManipulation()

    def __call__(self, auth: Dict, body: Dict) -> None:

        if not auth.get('Authorization'):
            raise UserNotAuthenticated('Token de acesso não encontrado.')

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

        if not body.get('title'):
            raise MissingParameter('Título')

        if not body.get('start_date'):
            raise MissingParameter('Data de início')

        if not body.get('end_date'):
            raise MissingParameter('Data de encerramento')

        if not body.get('start_amount'):
            raise MissingParameter('Lance inicial')

        if not body.get('images'):
            raise MissingParameter('Imagens')

        if not isinstance(body.get('start_amount'), int) and not isinstance(body.get('start_amount'), float):
            raise InvalidParameter('Lance inicial', 'deve ser um número')

        if body.get('start_amount') < 0:
            raise InvalidParameter('Lance inicial', 'não pode ser menor que zero')

        if body.get('start_date') < TimeManipulation.get_current_time():
            raise InvalidParameter('Data de início', 'não pode ser menor que a data atual')

        if body.get('end_date') < TimeManipulation.get_current_time():
            raise InvalidParameter('Data de encerramento', 'não pode ser menor que a data atual')

        if body.get('start_date') == body.get('end_date'):
            raise InvalidParameter('Data de início e encerramento', 'não podem ser iguais')

        if body.get('start_date') < TimeManipulation().plus_minute(4):
            raise InvalidParameter('Data de início', 'deve ser pelo menos 5 minutos maior que a data atual')

        if body.get('start_date') > body.get('end_date'):
            raise InvalidParameter('Data de início', 'não pode ser maior que a data de encerramento')

        last_auction_id = self.__auction_interface.get_last_auction_id()
        auction_id = last_auction_id + 1 if last_auction_id else 1

        auction = Auction(
            auction_id=str(auction_id),
            created_by=user['user_id'],
            title=body.get('title'),
            description=body.get('description'),
            start_date=body.get('start_date'),
            end_date=body.get('end_date'),
            start_amount=float(body.get('start_amount')),
            current_amount=float(body.get('start_amount')),
            images=body.get('images'),
            status_auction=STATUS_USER_ACCOUNT_ENUM.PENDING.value,
            created_at=TimeManipulation.get_current_time()
        )

        if self.__auction_interface.get_auction_between_dates(auction.start_date, auction.end_date):
            raise DataAlreadyUsed('Já existe um leilão cadastrado para esse período.')

        if auction.images:
            self.__image_manipulation.create_auction_folder(auction_id=auction.auction_id)
            for image in body.get('images'):
                response = self.__image_manipulation.upload_auction_image(auction_id=auction.auction_id,
                                                                          image_id=image.get('image_id'),
                                                                          image_body=image.get('image_body'),
                                                                          content_type=image.get('content_type'))
                image['image_body'] = response

        self.__auction_interface.create_auction(auction)

        time_now = TimeManipulation().plus_hour(3)
        notification_date = TimeManipulation(time_now=auction.start_date).plus_minute(-10)
        payload = {
            'body': {
                'auction_id': auction.auction_id,
                'time_now': time_now
            }
        }
        if time_now > notification_date:
            self.__trigger.invoke_lambda(lambda_function=f"start_auction", payload=payload)

        else:
            self.__trigger.create_trigger(rule_name=f"start_auction_{auction.auction_id}_before",
                                          lambda_function=f"start_auction",
                                          payload=payload,
                                          date=notification_date)

        payload['body'].pop('time_now')
        self.__trigger.create_trigger(rule_name=f"start_auction_{auction.auction_id}",
                                      lambda_function=f"start_auction",
                                      payload=payload,
                                      date=auction.start_date)

        return None
