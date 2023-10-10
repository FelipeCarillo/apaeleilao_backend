from typing import Dict


class CreateAuctionViewModel:
    def __call__(self, body: Dict) -> Dict:
        auction = body["body"]
        return{
            "auction": {
                "auction_id": auction["auction_id"],
                "user_id": auction["user_id"],
                "title": auction["title"],
                "description": auction["description"],
                "initial_value": auction["initial_value"],
                "status": auction["status"],
                "date_start": auction["date_start"],
                "date_end": auction["date_end"],
                "created_at": auction["created_at"],
            }
        }