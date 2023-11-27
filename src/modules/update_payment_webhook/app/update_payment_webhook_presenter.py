from .update_payment_webhook_usecase import UpdatePaymentWebhookUseCase
from .update_payment_webhook_controller import UpdatePaymentWebhookController

from src.shared.database.database_user import UserDynamodb
from src.shared.database.database_auction import AuctionDynamodb
from src.shared.https_codes.https_code import HttpResponse, HttpRequest

usecase = UpdatePaymentWebhookUseCase(AuctionDynamodb(), UserDynamodb())
controller = UpdatePaymentWebhookController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(auth=event["headers"], body=event["body"])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict("https://www.mercadopago.com.ar")
