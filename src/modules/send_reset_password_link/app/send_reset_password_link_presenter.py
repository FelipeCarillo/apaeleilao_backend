from .send_reset_password_link_usecase import SendResetPasswordLinkUseCase
from .send_reset_password_link_controller import SendResetPasswordLinkController

from src.shared.https_codes.https_code import HttpResponse, HttpRequest
from src.shared.database.database_user import UserDynamodb

usecase = SendResetPasswordLinkUseCase(UserDynamodb())
controller = SendResetPasswordLinkController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(body=event['queryStringParameters'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
