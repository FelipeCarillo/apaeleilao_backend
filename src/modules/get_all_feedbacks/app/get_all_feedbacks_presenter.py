from .get_all_feedbacks_usecase import GetAllFeedbacksUseCase
from .get_all_feedbacks_controller import GetAllFeedbacksController

from src.shared.database.database_user import UserDynamodb
from src.shared.https_codes.https_code import HttpResponse, HttpRequest

usecase = GetAllFeedbacksUseCase(UserDynamodb())
controller = GetAllFeedbacksController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(auth=event["headers"])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
