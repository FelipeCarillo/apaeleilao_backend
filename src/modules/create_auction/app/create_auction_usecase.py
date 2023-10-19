import uuid

from typing import Dict
from bcrypt import hashpw, gensalt

from src.shared.structure.entities.auction import Auction
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.helper_functions.time_manipulation import TimeManipulation
from src.shared.structure.interface.auction_interface import AuctionInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM, TYPE_ACCOUNT_USER_ENUM
from src.shared.errors.modules_errors import DataAlreadyUsed, MissingParameter, UserNotAuthenticated


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

        if not body.get('images'):
            raise MissingParameter('Imagens')

        auction = Auction(
            auction_id=str(uuid.uuid4()),
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

        

        type_account_need_permission = [TYPE_ACCOUNT_USER_ENUM.ADMIN, TYPE_ACCOUNT_USER_ENUM.MODERATOR]
        type_account = body.get('type_account', 'USER')
        status_account = STATUS_USER_ACCOUNT_ENUM.PENDING.value
        if TYPE_ACCOUNT_USER_ENUM(type_account) in type_account_need_permission:
            if not auth:
                raise MissingParameter('auth')
            if not auth.get('Authorization'):
                raise MissingParameter('Authorization')
            user_id = self.__token.decode_token(auth.get('Authorization')).get('user_id')
            if not user_id:
                raise UserNotAuthenticated()
            user = self.__user_interface.get_user_by_id(user_id)
            if not user:
                raise UserNotAuthenticated()
            if user.get('type_account') != TYPE_ACCOUNT_USER_ENUM.ADMIN.value:
                raise UserNotAuthenticated()
            status_account = STATUS_USER_ACCOUNT_ENUM.ACTIVE.value

        user_id = str(uuid.uuid4())
        date_joined = TimeManipulation.get_current_time()

        user.password = hashpw(user.password.encode('utf-8'), gensalt()).decode('utf-8')

        token = self.__token.generate_token(user_id=user_id, keep_login=True)

        self.__user_interface.create_user(user.to_dict())

        return {"token": token}
