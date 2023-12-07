from .get_all_auctions_menu_usecase import GetAllAuctionsMenuUseCase
from .get_all_auctions_menu_controller import GetAllAuctionsMenuController

from src.shared.https_codes.https_code import HttpResponse
from src.shared.database.database_auction import AuctionDynamodb

usecase = GetAllAuctionsMenuUseCase(AuctionDynamodb())
controller = GetAllAuctionsMenuController(usecase)


def lambda_handler(event, context):
    response = controller()
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
