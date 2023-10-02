import os
import json
from create_user_usecase import CreateUserUseCase
from src.shared.https_codes.https_code import HttpResponse
from create_user_controller import CreateUserController
from src.shared.database.user_dynamodb import UserDynamodb

usecase = CreateUserUseCase(UserDynamodb())
controller = CreateUserController(usecase)


def lambda_handler(event, context):
    stage = os.environ.get("STAGE")
    request = json.loads(json.dumps(event))
    status_code, body = controller(request=request).values()
    response = HttpResponse(status_code=status_code, body=body
                            )

    return response.data


if __name__ == '__main__':
    event = {
          "hearder":{
              "Content-Type": "application/json"
          },
          "body": {
            "first_name": "Ana Clara",
            "last_name": "Braga",
            "email": "23.00765-6@maua.br",
            "cpf": "73914804017",
            "phone": "11999885462",
            "password": "651gfsdf-1686ada-ad4adas",
            "accepted_terms": True,
            "is_verified": True
          }
    }
    context = {}

    response = lambda_handler(event, context)
    print(response)
