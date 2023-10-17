from .confirm_password_reset_code_usecase import ConfirmPasswordResetCodeUseCase
from .confirm_password_reset_code_controller import ConfirmVerificationEmailCodeController

from src.shared.database.database_user_table import UserDynamodb
from src.shared.https_codes.https_code import HttpResponse, HttpRequest

usecase = ConfirmPasswordResetCodeUseCase(UserDynamodb())
controller = ConfirmVerificationEmailCodeController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(auth=event['headers'], body=event['body'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
