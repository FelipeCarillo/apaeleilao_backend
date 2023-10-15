import os

from .authentificate_user_usecase import AuthentificateUserUseCase
from .authentificate_user_controller import AuthentificateUserController

from src.shared.database.database_user_table import UserDynamodb
from src.shared.https_codes.https_code import HttpResponse, HttpRequest


stage = os.environ.get("STAGE", "test")
usecase = AuthentificateUserUseCase(UserDynamodb())
controller = AuthentificateUserController(usecase)

def lambda_handler(event, context):
    request = HttpRequest(auth=event['queryStringParameters'], body=event['body'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()

