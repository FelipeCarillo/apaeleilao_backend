import pytest

from src.shared.structure.entities.auction import Auction, UserEntityError

class Teste_Auction:
    def teste_auction(self):
        auction = Auction(auction_id="1231231123", user_id="12321311421", title="Fusca", description="Cor azul",initial_value=100.00, current_value=1000.00, status="ACTIVE", date_start=1010, date_end=1510, bids=[100.00, 150.00, 1000.00], created_at=10)

        assert auction.auction_id == "1231231123"
        assert auction.user_id == "12321311421"
        assert auction.title == "Fusca"
        assert auction.description == "Cor azul"
        assert auction.initial_value == 100.00
        assert auction.current_value == 1000.00
        assert auction.status == "ACTIVE"
        assert auction.date_start == 1010
        assert auction.date_end == 1510
        assert auction.bids == [100.00, 150.00, 1000.00]
        assert auction.created_at == 10
    def teste_auction_id_is_none(self):
        with pytest.raises(UserEntityError):
            Auction(auction_id=None, user_id="12321311421", 
                   title="Fusca", 
                   description="Cor azul", initial_value=100.00, current_value=1000.00, status="ACTIVE", date_start=1010, date_end=1510, bids=[100.00, 150.00, 1000.00], created_at=10)
    
    def teste_auction_id_is_not_str(self):
        with pytest.raises(UserEntityError):
            Auction(auction_id=123123321, user_id="12321311421", 
                   title="Fusca", 
                   description="Cor azul", initial_value=100.00, current_value=1000.00, status="ACTIVE", date_start=1010, date_end=1510, bids=[100.00, 150.00, 1000.00], created_at=10)