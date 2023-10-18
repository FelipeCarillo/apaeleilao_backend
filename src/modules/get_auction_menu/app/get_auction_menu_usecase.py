from typing import Dict

from src.shared.structure.entities.user import Auction
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.auction_interface import AuctionInterface
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM
from src.shared.errors.modules_errors import *

class GetAuctionMenuUseCase:
    def __init__(self, auction_interface: AuctionInterface):
        self.__auction_interface = auction_interface
        self.__token = TokenAuthy()

    def __call__(self, body: Dict) -> Dict:
        if not body.get('Authorization'):
            raise MissingParameter('Authorization')
        
        decoded_token = self.__token.decode_token(body["Authorization"])
        if not decoded_token:
            raise DataNotFound("Token não encontrado.")
        auction_id = decoded_token.get('auction_id')
        auction = self.__auction_interface.get_auction_by_id(auction_id=auction_id)
        if not auction:
            raise DataNotFound("Leilão não encontrado.")
        
        status_auction_permitted = [STATUS_AUCTION_ENUM.OPEN, STATUS_AUCTION_ENUM.CLOSED, STATUS_AUCTION_ENUM.SUSPENDED]

        if STATUS_AUCTION_ENUM(auction.get('status_auction')) not in status_auction_permitted:
            raise DataNotFound(message='Leilão foi deletado.')
        
        auction = Auction(
            auction_id=auction["auction_id"], 
            title=auction.get("title"),
            description=auction.get("description"),
            initial_price=auction.get("initial_price"),
            status_auction=auction.get("status_auction"),
            status_payment=auction.get("status_payment"),
            date_start=int(auction.get("date_start")) if auction.get("date_start") else None,
            date_end=int(auction.get("date_end")) if auction.get("date_end") else None,
            bids=auction.get("bids"),
            winner=auction.get("winner"),
            seller=auction.get("seller"),
            created_at=int(auction.get("created_at")) if auction.get("created_at") else None,
            updated_at=int(auction.get("updated_at")) if auction.get("updated_at") else None
        )

        return auction.to_dict()
        


