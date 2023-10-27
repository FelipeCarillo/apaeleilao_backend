from .send_verification_email_code_controller import SendVerificationEmailCodeController
from .send_verification_email_code_usecase import SendVerificationEmailCodeUseCase

from src.shared.https_codes.https_code import HttpResponse, HttpRequest
from src.shared.database.database_user import UserDynamodb

usecase = SendVerificationEmailCodeUseCase(UserDynamodb())
controller = SendVerificationEmailCodeController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(auth=event['headers'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
