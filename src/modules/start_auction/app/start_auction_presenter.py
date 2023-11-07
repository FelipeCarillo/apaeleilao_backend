from .start_auction_usecase import StartAuctionUseCase
from .start_auction_controller import StartAuctionController

from src.shared.https_codes.https_code import HttpRequest, HttpResponse
from src.shared.database.database_user import UserDynamodb
from src.shared.database.database_auction import AuctionDynamodb

usecase = StartAuctionUseCase(AuctionDynamodb(), UserDynamodb())
controller = StartAuctionController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(body=event["body"])
    response = controller(request=request())
    response = HttpResponse(status_code=response.status_code, body=response.body)

    return response.to_dict()
