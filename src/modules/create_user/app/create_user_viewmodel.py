from typing import Dict


class CreateUserViewModel:
    def __call__(self, body: Dict) -> Dict:
        user = body['body']
        return {
            'user': {
                'email': user['email'],
                'password': user['password'],
                'type_account': user['type_account'],
            }
        }
