from .end_auction_usecase import EndAuctionUseCase
from .end_auction_controller import EndAuctionController

from src.shared.database.database_user import UserDynamodb
from src.shared.database.database_auction import AuctionDynamodb
from src.shared.https_codes.https_code import HttpRequest, HttpResponse

usecase = EndAuctionUseCase(AuctionDynamodb(), UserDynamodb())
controller = EndAuctionController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(body=event["body"])
    response = controller(request=request())
    response = HttpResponse(status_code=response.status_code, body=response.body)

    return response.to_dict()
