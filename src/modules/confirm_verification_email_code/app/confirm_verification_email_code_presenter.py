import os

from .confirm_verification_email_code_usecase import ConfirmVerificationEmailCodeUseCase
from .confirm_verification_email_code_controller import ConfirmVerificationEmailCodeController

from src.shared.database.database_user import UserDynamodb
from src.shared.https_codes.https_code import HttpResponse, HttpRequest

stage = os.environ.get("STAGE", "test")
usecase = ConfirmVerificationEmailCodeUseCase(UserDynamodb())
controller = ConfirmVerificationEmailCodeController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(auth=event['headers'], body=event['body'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
