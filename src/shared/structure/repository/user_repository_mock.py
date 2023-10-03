from time import time
from typing import Dict, Optional, List
from src.shared.structure.entities.user import User
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM


class UserRepositoryMock(UserInterface):
    def __init__(self):
        self.users = [
            User(user_id='dd0ba02b-1201-4c01-897b-9409522b2c7d',
                 first_name='Felipe', last_name='Carillo', cpf='12345678901',
                 email='felipecarillo@outlook.com', password='123456', phone='11999999999',
                 accepted_terms=True, status_account=STATUS_USER_ACCOUNT_ENUM.PENDING, suspensions=[],
                 date_joined=int(time()), verification_code=None, verification_code_expires_at=int(time()) + 3600,
                 password_reset_code=None, password_reset_code_expires_at=None),
        ]

    def authenticate(self, user_id: str, password: str) -> Optional[Dict]:
        for user in self.users:
            if user.user_id == user_id and user.password == password:
                return user.to_dict()
        return None

    def get_all_users(self) -> Optional[List[Dict]]:
        return [user.to_dict() for user in self.users]

    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        for user in self.users:
            if user.user_id == user_id:
                return user.to_dict()
        return None

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
        self.users.append(user)
        return user.to_dict()

    def update_user(self, user: User) -> Optional[Dict]:
        for i, user in enumerate(self.users):
            if user.user_id == user.user_id:
                self.users[i] = user
                return user.to_dict()
        return None



