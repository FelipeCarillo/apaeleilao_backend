from src.shared.structure.entities.user import User
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM
from src.shared.errors.controller_errors import MissingParameter, UserNotAuthenticated


class GetUserUseCase:
    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface

    def __call__(self, email: str, password: str, user_id: str = None) -> User:
        if not email:
            raise MissingParameter('email')
        if not password:
            raise MissingParameter('password')

        auth = self.__user_interface.authenticate(email=email, password=password, user_id=user_id)
        if not auth:
            raise UserNotAuthenticated()

        user_id = auth['user_id']
        first_name = auth['first_name']
        last_name = auth['last_name']
        cpf = auth['cpf']
        email = auth['email']
        phone = auth['phone']
        password = auth['password']
        accepted_terms = auth['accepted_terms']
        status_account = STATUS_USER_ACCOUNT_ENUM(auth['status_account'])
        suspensions = auth['suspensions']
        date_joined = int(auth['date_joined'])
        verification_email_code = int(auth['verification_email_code'])
        verification_email_code_expires_at = int(auth['verification_email_code_expires_at'])
        password_reset_code = int(auth['password_reset_code'])
        password_reset_code_expires_at = int(auth['password_reset_code_expires_at'])

        user = User(user_id=user_id, first_name=first_name, last_name=last_name, cpf=cpf, email=email, phone=phone,
                    password=password, accepted_terms=accepted_terms, status_account=status_account,
                    suspensions=suspensions, date_joined=date_joined, verification_email_code=verification_email_code,
                    verification_email_code_expires_at=verification_email_code_expires_at,
                    password_reset_code=password_reset_code,
                    password_reset_code_expires_at=password_reset_code_expires_at)

        return user
