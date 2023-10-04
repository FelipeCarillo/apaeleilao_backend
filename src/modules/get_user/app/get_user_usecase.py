from src.shared.structure.entities.user import User
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM
from src.shared.errors.controller_errors import MissingParameter, UserNotAuthenticated


class GetUserUseCase:
    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface

    def __call__(self, user_id: str = None, email: str = None, cpf: str = None, password: str = None) -> User:
        if not email and not cpf and not user_id:
            raise MissingParameter('email or cpf')
        if not password:
            raise MissingParameter('password')

        auth = self.__user_interface.authenticate(user_id=user_id, email=email, cpf=cpf, password=password)
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
        date_joined = auth['date_joined']
        verification_code = auth['verification_code']
        verification_code_expires_at = auth['verification_code_expires_at']
        password_reset_code = auth['password_reset_code']
        password_reset_code_expires_at = auth['password_reset_code_expires_at']

        user = User(user_id=user_id, first_name=first_name, last_name=last_name, cpf=cpf, email=email, phone=phone,
                    password=password, accepted_terms=accepted_terms, status_account=status_account,
                    suspensions=suspensions, date_joined=date_joined, verification_code=verification_code,
                    verification_code_expires_at=verification_code_expires_at, password_reset_code=password_reset_code,
                    password_reset_code_expires_at=password_reset_code_expires_at)

        return user
