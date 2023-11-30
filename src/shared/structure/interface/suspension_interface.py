from abc import ABC, abstractmethod
from typing import Optional, Dict, List

from src.shared.structure.entities.suspension import Suspension
from src.shared.structure.entities.user import User, UserModerator
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM
from src.shared.structure.enums.suspension_enum import STATUS_SUSPENSION_ENUM



class SuspensionInterface(ABC):

    @abstractmethod
    def get_suspension_by_id(self, suspension_id: str) -> Optional[Dict]:
        """
        Get a suspension by id
        """
        pass