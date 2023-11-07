from abc import ABC, abstractmethod
from typing import Optional, Dict

from src.shared.structure.entities.suspension import Suspension
from src.shared.structure.entities.user import User, UserModerator


class UserInterface(ABC):

    @abstractmethod
    def authenticate(self,
                     access_key: str = None,
                     email: str = None,
                     ) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_all_users(self, exclusive_start_key: str = None, limit: int = None,
                      type_account: str = 'USER') -> Optional[Dict]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_user_by_cpf(self, cpf: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_user_by_access_key(self, access_key: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def create_user(self, user: User or UserModerator) -> Optional[Dict]:
        pass

    @abstractmethod
    def update_user(self, user: User) -> Optional[Dict]:
        pass

    @abstractmethod
    def create_suspension(self, suspension: Suspension) -> Optional[Dict]:
        pass
