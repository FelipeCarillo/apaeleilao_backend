from typing import Dict


class AuthentificateUserViewModel:
    def __call__(self, body: Dict) -> Dict:
        user = body['body']
        return {
            'email': user['email'],
            'password': user['password'],
        }
