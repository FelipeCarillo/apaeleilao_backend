import os
import json
from .create_user_usecase import CreateUserUseCase
from src.shared.https_codes.https_code import HttpResponse
from .create_user_controller import CreateUserController
from src.shared.database.user_dynamodb import UserDynamodb

usecase = CreateUserUseCase(UserDynamodb())
controller = CreateUserController(usecase)


def lambda_handler(event, context):

    stage = os.environ.get("STAGE")
    request = json.loads(json.dumps(event))
    status_code, body = controller(request=request)
    response = HttpResponse(status_code=status_code, body=body).data

    return response

