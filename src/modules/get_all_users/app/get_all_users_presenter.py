from .get_all_users_usecase import GetAllUsersUseCase
from .get_all_users_controller import GetAllUsersController

from src.shared.database.database_user import UserDynamodb
from src.shared.https_codes.https_code import HttpResponse, HttpRequest

usecase = GetAllUsersUseCase(UserDynamodb())
controller = GetAllUsersController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(auth=event["headers"])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
