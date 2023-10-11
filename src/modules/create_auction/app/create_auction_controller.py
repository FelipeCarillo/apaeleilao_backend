from typing import Dict

from .create_auction_usecase import CreateAuctionUseCase
from .create_auction_viewmodel import CreateAuctionViewModel

from src.shared.https_codes.https_code import Created, BadRequest, InternalServerError, ParameterError
from src.shared.errors.modules_errors import InvalidRequest, MissingParameter, InvalidParameter, DataAlreadyUsed


class CreateAuctionController:
    def __init__(self, usecase: CreateAuctionUseCase):
        self.__usecase = usecase
        self.__viewmodel = CreateAuctionViewModel()

    def __call__(self, request: Dict):
        try:
            if not request:
                raise InvalidRequest()

            if not request.get("body"):
                raise MissingParameter("body")

            create_auction_usecase = self.__usecase(request=request["body"])

            response = self.__viewmodel(create_auction_usecase)

            return Created(response, message="Leilão criado com sucesso.")

        except DataAlreadyUsed as e:
            return ParameterError(message=e.message)

        except InvalidRequest as e:
            return BadRequest(message=e.message)

        except InvalidParameter as e:
            return ParameterError(message=e.message)

        except MissingParameter as e:
            return BadRequest(message=e.message)

        except Exception as e:
            return InternalServerError(message=e.args[0])
