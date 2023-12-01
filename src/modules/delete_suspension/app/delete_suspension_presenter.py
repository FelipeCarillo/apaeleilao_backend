from .delete_suspension_usecase import DeleteSuspensionUseCase
from .delete_suspension_controller import DeleteSuspensionController

from src.shared.database.database_user import UserDynamodb
from src.shared.https_codes.https_code import HttpResponse, HttpRequest

usecase = DeleteSuspensionUseCase(UserDynamodb())
controller = DeleteSuspensionController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(auth=event['headers'], body=event['queryStringParameters'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()