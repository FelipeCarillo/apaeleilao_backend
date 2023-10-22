from typing import Dict

from src.shared.structure.entities.auction import Auction
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.helper_functions.time_manipulation import TimeManipulation
from src.shared.helper_functions.image_manipulation import ImageManipulation
from src.shared.structure.interface.auction_interface import AuctionInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM, TYPE_ACCOUNT_USER_ENUM
from src.shared.errors.modules_errors import DataAlreadyUsed, MissingParameter, UserNotAuthenticated, InvalidParameter


class CreateUserUseCase:
    def __init__(self, user_interface: UserInterface, auction_interface: AuctionInterface):
        self.__user_interface = user_interface
        self.__auction_interface = auction_interface
        self.__token = TokenAuthy()

    def __call__(self, auth: Dict, body: Dict) -> Dict:

        if not auth.get('Authorization'):
            raise MissingParameter('Authorization')

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

        if not body.get('tittle'):
            raise MissingParameter('Título')

        if not body.get('start_date'):
            raise MissingParameter('Data de início')

        if not body.get('end_date'):
            raise MissingParameter('Data de encerramento')

        if not body.get('start_amount'):
            raise MissingParameter('Lance inicial')
        if body.get('start_amount') < 0:
            raise InvalidParameter('Lance inicial', 'não pode ser menor que zero.')

        if body.get('start_date') > body.get('end_date'):
            raise InvalidParameter('Data de início', 'não pode ser maior que a data de encerramento.')

        last_auction_id = self.__auction_interface.get_last_auction_id()
        auction_id = last_auction_id + 1 if last_auction_id else 1

        auction = Auction(
            auction_id=str(auction_id),
            created_by=user['user_id'],
            tittle=body.get('tittle'),
            description=body.get('description'),
            start_date=body.get('start_date'),
            end_date=body.get('end_date'),
            start_amount=body.get('start_amount'),
            current_amount=body.get('start_amount'),
            images=body.get('images'),
            status_auction=STATUS_USER_ACCOUNT_ENUM.PENDING.value,
            create_at=TimeManipulation.get_current_time()
        )

        if self.__auction_interface.get_auction_between_dates(auction.start_date, auction.end_date):
            raise DataAlreadyUsed('Já existe um leilão cadastrado para esse período.')

        if body.get('images'):
            ImageManipulation().create_auction_folder(auction_id=auction.auction_id)
            for image in body.get('images'):
                image_id = image.get('image_id').split(".")
                image_body = image.get('image_body')
                response = ImageManipulation().upload_auction_image(image_id=image_id[0], image_body=image_body,
                                                                    content_type=image_id[-1])
                image['image_body'] = response

        self.__auction_interface.create_auction(auction)

        return {'auction_id': auction.auction_id}
