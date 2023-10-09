from abc import ABC, abstractmethod
from typing import Optional, Dict

from src.shared.structure.entities.user import User


class UserInterface(ABC):

    @abstractmethod
    def authenticate(self, email: str, password: str) -> Optional[Dict]:
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
    def create_user(self, user: User) -> Optional[Dict]:
        pass

    @abstractmethod
    def update_user(self, email: str, **kwargs) -> Optional[Dict]:
        pass
