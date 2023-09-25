from abc import ABC, abstractmethod

from src.shared.structure.entities.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, id_user: str) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def get_user_by_cpf(self, cpf: str) -> User:
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_all_users(self) -> list:
        pass

    @abstractmethod
    def get_duplicated_users(self) -> list:
        pass

    @abstractmethod

