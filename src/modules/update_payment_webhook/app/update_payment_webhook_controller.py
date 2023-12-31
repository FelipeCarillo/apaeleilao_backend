from .update_payment_webhook_usecase import UpdatePaymentWebhookUseCase

from src.shared.errors.modules_errors import *
from src.shared.https_codes.https_code import *


class UpdatePaymentWebhookController:
    def __init__(self, usecase: UpdatePaymentWebhookUseCase):
        self.__usecase = usecase

    def __call__(self, request: Dict):
        try:
            if not request:
                raise InvalidRequest()

            if not request.get("body"):
                raise MissingParameter("body")

            update_user_usecase = self.__usecase(body=request["body"])

            return OK(body=update_user_usecase, message="Dados alterados com sucesso.")

        except InvalidRequest as e:
            return BadRequest(message=e.message)

        except MissingParameter as e:
            return BadRequest(message=e.message)

        except InvalidParameter as e:
            return ParameterError(message=e.message)

        except UserNotAuthenticated as e:
            return Unauthorized(message=e.message)

        except Exception as e:
            return InternalServerError(message=e.args[0])
