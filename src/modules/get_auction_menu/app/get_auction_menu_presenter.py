from .get_auction_menu_controller import GetAuctionMenuController
from .get_auction_menu_usecase import GetAuctionMenuUseCase

from src.shared.https_codes.https_code import HttpResponse, HttpRequest
from src.shared.database.database_auction_table import AuctionDynamodb

usecase = GetAuctionMenuUseCase(AuctionDynamodb())
controller = GetAuctionMenuController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(auth=event['headers'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()