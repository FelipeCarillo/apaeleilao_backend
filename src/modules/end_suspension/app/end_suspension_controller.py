from .end_suspension_usecase import EndSuspensionUseCase

from src.shared.errors.modules_errors import *
from src.shared.https_codes.https_code import *


class EndSuspensionController:
    def __init__(self, usecase: EndSuspensionUseCase):
        self.__usecase = usecase

    def __call__(self, request: Dict):
        try:
            if not request:
                raise InvalidRequest()

            if not request["body"]:
                raise MissingParameter("body")

            usecase = self.__usecase(body=request["body"])

            return OK(body=usecase, message="Suspensão finalizada com sucesso!")

        except InvalidRequest as e:
            return BadRequest(message=e.message)

        except MissingParameter as e:
            return BadRequest(message=e.message)

        except InvalidParameter as e:
            return ParameterError(message=e.message)

        except DataNotFound as e:
            return NotFound(message=e.message)

        except UserNotAuthenticated as e:
            return Unauthorized(message=e.message)

        except Exception as e:
            return InternalServerError(message=e.args[0])