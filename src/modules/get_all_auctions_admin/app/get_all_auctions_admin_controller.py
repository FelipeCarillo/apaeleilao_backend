from .get_all_auctions_admin_usecase import GetAllAuctionsAdminUseCase

from src.shared.errors.modules_errors import *
from src.shared.https_codes.https_code import *


class GetAllAuctionsAdminController:
    def __init__(self, usecase: GetAllAuctionsAdminUseCase):
        self.__usecase = usecase

    def __call__(self, request: Dict):
        try:
            if not request:
                raise InvalidRequest()

            if not request.get('auth'):
                raise MissingParameter('auth')

            usecase = self.__usecase(auth=request.get('auth'), body=request.get('body'))

            return OK(body=usecase, message="Leilões encontrados com sucesso.")

        except DataNotFound as e:
            return NotFound(message=e.message)

        except InvalidRequest as e:
            return BadRequest(message=e.message)

        except UserNotAuthenticated as e:
            return Unauthorized(message=e.message)

        except InvalidParameter as e:
            return ParameterError(message=e.message)

        except MissingParameter as e:
            return BadRequest(message=e.message)

        except Exception as e:
            return InternalServerError(message=e.args[0])
