from .get_token_usecase import GetTokenUseCase
from .get_token_controller import GetTokenController

from src.shared.https_codes.https_code import HttpResponse, HttpRequest
from src.shared.database.database_user import UserDynamodb

usecase = GetTokenUseCase(UserDynamodb())
controller = GetTokenController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(body=event['body'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
