from .create_feedback_usecase import CreateFeedbackUseCase
from .create_feedback_controller import CreateFeedbackController

from src.shared.database.database_user import UserDynamodb
from src.shared.database.database_auction import AuctionDynamodb
from src.shared.https_codes.https_code import HttpResponse, HttpRequest

usecase = CreateFeedbackUseCase(UserDynamodb(), AuctionDynamodb())
controller = CreateFeedbackController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(auth=event['headers'], body=event['body'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
