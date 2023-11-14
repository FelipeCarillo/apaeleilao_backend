from .delete_auction_usecase import DeleteAuctionUseCase
from .delete_auction_controller import DeleteAuctionController

from src.shared.database.database_user import UserDynamodb
from src.shared.database.database_auction import AuctionDynamodb
from src.shared.https_codes.https_code import HttpResponse, HttpRequest

usecase = DeleteAuctionUseCase(UserDynamodb(), AuctionDynamodb())
controller = DeleteAuctionController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(auth=event['headers'], body=event['queryStringParameters'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
