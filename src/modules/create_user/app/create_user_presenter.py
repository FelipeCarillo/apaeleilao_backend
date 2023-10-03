import os
import json
from .create_user_usecase import CreateUserUseCase
from src.shared.https_codes.https_code import HttpResponse
from .create_user_controller import CreateUserController
from src.shared.database.database_user_table import UserDynamodb

usecase = CreateUserUseCase(UserDynamodb())
controller = CreateUserController(usecase)


def lambda_handler(event, context):
    stage = os.environ.get("STAGE")
    request = json.loads(json.dumps(event))
    response = controller(request=request)
    http = HttpResponse(status_code=response.status_code, body=response.body)

    return http.to_dict()
