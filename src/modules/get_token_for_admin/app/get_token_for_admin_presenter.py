import os

from .get_token_for_admin_usecase import GetTokenUseCase
from .get_token_for_admin_controller import GetTokenController

from src.shared.https_codes.https_code import HttpResponse, HttpRequest
from src.shared.database.database_user import UserDynamodb

stage = os.environ.get("STAGE", "test")
usecase = GetTokenUseCase(UserDynamodb())
controller = GetTokenController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(body=event['body'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
