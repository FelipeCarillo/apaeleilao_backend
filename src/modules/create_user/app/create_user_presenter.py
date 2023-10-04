import os
import json
from .create_user_controller import CreateUserController
from .create_user_usecase import CreateUserUseCase
from src.shared.https_codes.https_code import HttpResponse
from src.shared.database.database_user_table import UserDynamodb
from src.shared.structure.repository.user_repository_mock import UserRepositoryMock


stage = os.environ.get("STAGE", "test")
if stage == "test":
    usecase = CreateUserUseCase(UserRepositoryMock())
else:
    usecase = CreateUserUseCase(UserDynamodb())
controller = CreateUserController(usecase)


def lambda_handler(event, context):
    request = json.loads(event['body'])
    response = controller(request=request)
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
