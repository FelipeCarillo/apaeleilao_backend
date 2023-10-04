from typing import Dict


class CreateUserViewModel:
    def __call__(self, body: Dict) -> Dict:
        return {
            'user': {
                'user_id': body['user_id'],
                'email': body['email'],
                'password': body['password'],
            }
        }
