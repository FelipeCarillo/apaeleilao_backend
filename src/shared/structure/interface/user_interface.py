from abc import ABC, abstractmethod
from typing import Optional, Dict

from src.shared.structure.entities.user import User


class UserInterface(ABC):

    @abstractmethod
    def authenticate(self,
                     user_id: str = None,
                     email: str = None,
                     password: str = None,
                     password_hash: str = None
                     ) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_all_users(self) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_user_by_cpf(self, cpf: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def create_user(self, user: Dict) -> Optional[Dict]:
        pass

    @abstractmethod
    def update_user(self, user: User) -> Optional[Dict]:
        pass
