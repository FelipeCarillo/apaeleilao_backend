from .get_auctions_menu_controller import GetAuctionsMenuController
from .get_auctions_menu_usecase import GetAuctionsMenuUseCase

from src.shared.https_codes.https_code import HttpResponse, HttpRequest
from src.shared.database.database_auction import AuctionDynamodb

usecase = GetAuctionsMenuUseCase(AuctionDynamodb())
controller = GetAuctionsMenuController(usecase)


def lambda_handler(event, context):
    request = HttpRequest()
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()