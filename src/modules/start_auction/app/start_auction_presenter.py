from .start_auction_usecase import StartAuctionUseCase
from .start_auction_controller import StartAuctionController

from src.shared.database.database_auction import AuctionDynamodb
from src.shared.https_codes.https_code import HttpRequest

usecase = StartAuctionUseCase(AuctionDynamodb())
controller = StartAuctionController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(body=event["body"])
    controller(request=request())
