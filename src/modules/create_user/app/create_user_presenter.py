from .create_user_usecase import CreateUserUseCase
from .create_user_controller import CreateUserController

from src.shared.database.database_user_table import UserDynamodb
from src.shared.https_codes.https_code import HttpResponse, HttpRequest

usecase = CreateUserUseCase(UserDynamodb())
controller = CreateUserController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(body=event['body'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
