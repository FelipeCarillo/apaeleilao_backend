import os
import json
from src.modules.create_user.app.create_user_controller import CreateUserController


def lambda_handler(event, context):
    stage = os.environ.get("STAGE")
    request = json.loads(event)

    response = CreateUserController(request)()

    return {
        'statusCode': response['statusCode'],
        'body': json.dumps(response['body'])
    }







