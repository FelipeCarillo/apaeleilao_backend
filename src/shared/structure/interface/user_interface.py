from abc import ABC, abstractmethod
from typing import Optional, Dict, List

from src.shared.structure.entities.feedback import Feedback
from src.shared.structure.entities.suspension import Suspension
from src.shared.structure.entities.user import User, UserModerator
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM


class UserInterface(ABC):

    @abstractmethod
    def authenticate(self,
                     access_key: str = None,
                     email: str = None,
                     ) -> Optional[Dict]:
        pass

    @abstractmethod
    def create_feedback(self,feedback: Feedback) -> Dict or None:
        """
        Create a new feedback
        """
        pass

    @abstractmethod
    def get_all_users(self, exclusive_start_key: str = None, limit: int = None,
                      type_account: List[str] = 'USER') -> Optional[Dict]:
        pass

    @abstractmethod
    def get_all_users_to_send_email(self) -> Optional[Dict]:
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
    def update_user_status(self, user_id: str, status: STATUS_USER_ACCOUNT_ENUM) -> Optional[Dict]:
        pass

    @abstractmethod
    def create_suspension(self, suspension: Suspension) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_all_suspensions_by_user_id(self, user_id: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_last_feedback_id(self) -> int:
        pass 
