import os
import json
from .create_user_usecase import CreateUserUseCase
from .create_user_controller import CreateUserController
from src.shared.database.user_dynamodb import UserDynamodb

usecase = CreateUserUseCase(UserDynamodb())
controller = CreateUserController(usecase)


def lambda_handler(event, context):

    stage = os.environ.get("STAGE")
    request = json.loads(json.dumps(event))
    response = controller(request=request)

    return {
        'statusCode': response['statusCode'],
        'body': json.dumps(response['body'])
    }
