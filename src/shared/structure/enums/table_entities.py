from enum import Enum


class USER_TABLE_ENTITY(Enum):
    USER = "USER"
    SUSPENSION = "SUSPENSION"
    FEEDBACK = "FEEDBACK"


class AUCTION_TABLE_ENTITY(Enum):
    AUCTION = "AUCTION"
    BID = "BID"
    PAYMENT = "PAYMENT"