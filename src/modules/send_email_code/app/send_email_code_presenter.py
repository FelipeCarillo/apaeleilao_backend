import os

from .send_email_code_controller import SendEmailCodeController
from .send_email_code_usecase import SendEmailCodeUseCase

from src.shared.https_codes.https_code import HttpResponse, HttpRequest
from src.shared.database.database_user_table import UserDynamodb

stage = os.environ.get("STAGE", "test")
usecase = SendEmailCodeUseCase(UserDynamodb())
controller = SendEmailCodeController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(auth=event['headers'], body=event['queryStringParameters'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
