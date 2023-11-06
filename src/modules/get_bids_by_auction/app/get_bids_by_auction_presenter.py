from .get_bids_by_auction_usecase import GetBidUseCase
from .get_bids_by_auction_controller import GetBidController

from src.shared.https_codes.https_code import HttpResponse, HttpRequest
from src.shared.database.database_user import UserDynamodb

usecase = GetBidUseCase(UserDynamodb())
controller = GetBidController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(auth=event['headers'], body=event['queryStringParameters'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
