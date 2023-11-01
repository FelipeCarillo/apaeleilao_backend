from typing import Any, Dict

from src.shared.errors.modules_errors import *
from src.shared.helper_functions.email_function import Email
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.auction_interface import AuctionInterface
from src.shared.structure.interface.user_interface import UserInterface

class StartAuctionUseCase:

    def __init__(self, auction_interface: AuctionInterface, user_interface: UserInterface):
        self.__auction_interface = auction_interface
        self.__user_interface = user_interface
        self.__token = TokenAuthy()
        self.__email = Email()
    
    def __call__(self, body: Dict) -> Any:
        
        if not body:
            raise MissingParameter('body')
        
        auction_id = body.get("auction_id")
        if not auction_id:
            raise MissingParameter('auction_id')
        
        auction = self.__auction_interface.get_auction_by_id(auction_id=auction_id)
        if not auction:
            raise DataNotFound('Leilão')
        
        users = self.__user_interface.get_all_users()

        to_email = [user.get("email") for user in users]

        if body.get("send_before"):
            email_body = f"""
            <h1>Leilão<span style="font-weight: bold;">{auction.title} LOTE[{auction.auction_id}]</span> Iniciará em 10 minutos!</h1><p>O leilão está prestes a começar.</p>
            <p>Para mais informações acesse o site.</p>
            """
            self.__email.set_email_template(f"Leilão {auction.title} Iniciará em 10 minutos!", 
                                            email_body)

            self.__email.send_email(to=to_email,
                                    subject="Leilão iniciará em 10 minutos")
        
        else:
            email_body = f"""
            <h1>Leilão<span style="font-weight: bold;">{auction.title} LOTE[{auction.auction_id}]</span> Começou!</h1><p>O leilão está aberto.</p>
            <p>Para mais informações acesse o site.</p>
            """
            self.__email.set_email_template(f"Leilão {auction.title} Começou!", 
                                            email_body)
            
            self.__email.send_email(to=to_email,
                                    subject="Leilão começou!")

