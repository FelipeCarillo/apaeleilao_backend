from .get_all_auctions_menu_usecase import GetAllAuctionsMenuUseCase

from src.shared.errors.modules_errors import *
from src.shared.https_codes.https_code import *


class GetAllAuctionsMenuController:
    def __init__(self, usecase: GetAllAuctionsMenuUseCase):
        self.__usecase = usecase

    def __call__(self):
        try:
            usecase = self.__usecase()

            return OK(body=usecase, message="Leilões encontrados com sucesso.")

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
