from typing import Dict


class CreateUserViewModel:
    def __call__(self, body: Dict) -> Dict:
        user = body['body']
        return {
            'user': {
                'user_id': user['user_id'],
                'email': user['email'],
                'password': user['password'],
            }
        }
