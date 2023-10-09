from typing import Dict

from src.shared.structure.entities.user import User


class GetUserViewModel:
    def __call__(self, user: User) -> Dict:
        return {
            'body': {
                'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'cpf': user.cpf,
                'email': user.email,
                'phone': user.phone,
                'accepted_terms': user.accepted_terms,
                'status_account': user.status_account.value,
                'suspensions': user.suspensions,
                'date_joined': user.date_joined,
                'verification_email_code': user.verification_email_code,
                'verification_email_code_expires_at': user.verification_email_code_expires_at,
                'password_reset_code': user.password_reset_code,
                'password_reset_code_expires_at': user.password_reset_code_expires_at,
            }
        }
