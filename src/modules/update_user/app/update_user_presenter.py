import os

from .update_user_usecase import UpdateUserUseCase
from .update_user_controller import UpdateUserController

from src.shared.database.database_user import UserDynamodb
from src.shared.https_codes.https_code import HttpResponse, HttpRequest

stage = os.environ.get("STAGE", "test")
usecase = UpdateUserUseCase(UserDynamodb())
controller = UpdateUserController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(auth=event["headers"], body=event["body"])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()