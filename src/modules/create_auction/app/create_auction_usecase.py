import os
import uuid
from time import time
from typing import Any, Dict

from src.shared.structure.entities.auction import Auction
from src.shared.errors.modules_errors import *
from src.shared.structure.enums.auction_enum import STATUS_AUCTION_ENUM
from src.shared.structure.interface.auction_interface import AuctionInterface


class CreateAuctionUseCase:
    def __init__(self, auction_interface: AuctionInterface):
        self.__auction_interface = auction_interface

    def __call__(self, request: Dict) -> Dict:

        if not request["auction_id"]:
            raise MissingParameter("auction_id")
        
        if not request["title"]:
            raise MissingParameter("title")
        
        auction_id = str(uuid.uuid4())

        auction = Auction(auction_id=auction_id, admin_id=request["auction_id"], title=request["title"],
                          description=request["description"], initial_value=request["initial_value"],
                          status=request["status"], date_start=request["date_start"], date_end=request["date_end"],
                          created_at=request["created_at"])

        return self.__auction_interface.create_auction(auction)