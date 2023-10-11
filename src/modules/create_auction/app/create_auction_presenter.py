import os

from .create_auction_usecase import CreateAuctionUseCase
from .create_auction_controller import CreateAuctionController

from src.shared.database.database_auction_table import AuctionDynamodb
from src.shared.https_codes.https_code import HttpResponse, HttpRequest

stage = os.environ.get("STAGE", "test")
usecase = CreateAuctionUseCase(AuctionDynamodb())
controller = CreateAuctionController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(body=event["body"])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()