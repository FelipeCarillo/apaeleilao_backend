from .get_user_usecase import GetUserUseCase
from .get_user_controller import GetUserController

from src.shared.https_codes.https_code import HttpResponse, HttpRequest
from src.shared.database.database_user_table import UserDynamodb

usecase = GetUserUseCase(UserDynamodb())
controller = GetUserController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(body=event['queryStringParameters'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
