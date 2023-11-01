from .end_auction_usecase import EndAuctionUseCase
from .end_auction_controller import EndAuctionController

from src.shared.database.database_auction import AuctionDynamodb
from src.shared.https_codes.https_code import HttpRequest

usecase = EndAuctionUseCase(AuctionDynamodb())
controller = EndAuctionController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(body=event["body"])
    controller(request=request())
