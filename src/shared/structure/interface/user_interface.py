from abc import ABC, abstractmethod
from typing import Optional, Any
from src.shared.structure.entities.user import User


class UserInterface(ABC):

    @abstractmethod
    def authenticate(self, user_id: str, password: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_all_users(self) -> Optional[Any]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    def get_user_by_cpf(self, cpf: str) -> Optional[User]:
        pass

    @abstractmethod
    def create_user(self, user: User):
        pass

    @abstractmethod
    def update_user(self, user: User):
        pass


