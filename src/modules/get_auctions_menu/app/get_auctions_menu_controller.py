from get_auctions_menu_usecase import GetAuctionsMenuUseCase

from src.shared.https_codes.https_code import *
from src.shared.errors.modules_errors import *


class GetAuctionsMenuController:
    def __init__(self, usecase: GetAuctionsMenuUseCase):
        self.__usecase = usecase

    def __call__(self):
        try:
            get_auction_menu_usecase = self.__usecase()

            return OK(body=get_auction_menu_usecase, message="Leilão encontrado com sucesso.")

        except DataNotFound as e:
            return NotFound(message=e.message)

        except InvalidRequest as e:
            return BadRequest(message=e.message)

        except InvalidParameter as e:
            return ParameterError(message=e.message)

        except MissingParameter as e:
            return BadRequest(message=e.message)

        except Exception as e:
            return InternalServerError(message=e.args[0])
