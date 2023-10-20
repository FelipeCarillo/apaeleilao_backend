from .send_password_reset_code_usecase import SendPasswordResetCodeUseCase
from .send_password_reset_code_controller import SendPasswordResetCodeController

from src.shared.https_codes.https_code import HttpResponse, HttpRequest
from src.shared.database.database_user import UserDynamodb

usecase = SendPasswordResetCodeUseCase(UserDynamodb())
controller = SendPasswordResetCodeController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(body=event['queryStringParameters'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
