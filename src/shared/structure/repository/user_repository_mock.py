from time import time
from cryptography.fernet import Fernet
from typing import Dict, Optional, List

from src.shared.structure.entities.user import User
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM


class UserRepositoryMock(UserInterface):
    def __init__(self):
        self.users = [
            User(user_id='dd0ba02b-1201-4c01-897b-9409522b2c7d',
                 first_name='Felipe', last_name='Carillo', cpf='37126329245',
                 email='felipecarillo@outlook.com', password='gAAAAABlJBTT8EW2D04_FdNGqHTvh-9xplm'
                                                             '-Dx4niO6s1xD8elBah6ia_NyJpb-QCFNzW7rPGnA2y4WcjnBpybk5'
                                                             '-DW38Su6pA==', phone='11999999999',
                 accepted_terms=True, status_account=STATUS_USER_ACCOUNT_ENUM.PENDING, suspensions=[],
                 date_joined=int(time()), verification_email_code=None, verification_email_code_expires_at=None,
                 password_reset_code=None, password_reset_code_expires_at=None),
        ]

    def authenticate(self, email: str, password: str, user_id: str = None) -> Optional[Dict]:

        encrypted_key = ''.encode('utf-8')
        f = Fernet(encrypted_key)

        for user in self.users:
            real_password = f.decrypt(user.password.encode('utf-8')).decode('utf-8')
            if user.email == email and real_password == password:
                return user.to_dict()

    def get_all_users(self) -> Optional[List[Dict]]:
        return [user.to_dict() for user in self.users]

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        for user in self.users:
            if user.email == email:
                return user.to_dict()
        return None

    def get_user_by_cpf(self, cpf: str) -> Optional[Dict]:
        for user in self.users:
            if user.cpf == cpf:
                return user.to_dict()
        return None

    def create_user(self, user: User) -> Optional[Dict]:
        user.status_account = user.status_account.value
        self.users.append(user)
        return user.to_dict()

    def update_user(self, user: User) -> Optional[Dict]:
        for i, user in enumerate(self.users):
            if user.user_id == user.user_id:
                self.users[i] = user
                return user.to_dict()
        return None


if __name__ == '__main__':
    user_repository_mock = UserRepositoryMock()
    print(user_repository_mock.authenticate(password='123456',
                                            email=user_repository_mock.users[0].email))
