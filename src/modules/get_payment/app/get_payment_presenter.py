from .get_payment_usecase import GetPaymentUseCase
from .get_payment_controller import GetPaymentController

from src.shared.database.database_user import UserDynamodb
from src.shared.database.database_auction import AuctionDynamodb
from src.shared.https_codes.https_code import HttpRequest, HttpResponse

usecase = GetPaymentUseCase(AuctionDynamodb(), UserDynamodb())
controller = GetPaymentController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(body=event["queryStringParameters"])
    response = controller(request=request())
    response = HttpResponse(status_code=response.status_code, body=response.body)

    return response.to_dict()
