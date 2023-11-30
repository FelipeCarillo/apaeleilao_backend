from abc import ABC

from src.shared.errors.modules_errors import InvalidParameter
from src.shared.structure.enums.suspension_enum import STATUS_SUSPENSION_ENUM


class Suspension(ABC):
    user_id: str
    suspension_id: str
    date_suspencion: int
    date_reactivation: int
    reason: str
    user_id: str
    status: STATUS_SUSPENSION_ENUM
    created_at: int

    def __init__(self, user_id: str = None, suspension_id: str = None, date_suspension: int = None, date_reactivation: int = None,
                 reason: str = None, status_suspension: STATUS_SUSPENSION_ENUM = None, created_at: int = None):
        self.user_id = user_id
        self.suspension_id = self.validade_and_set_suspension_id(suspension_id)
        self.date_suspension = self.validate_and_set_date_suspencion(date_suspension)
        self.date_reactivation = self.validate_and_set_date_reactivation(date_reactivation)
        self.reason = self.validate_and_set_reason(reason)
        self.status = self.validate_and_set_status_suspension(STATUS_SUSPENSION_ENUM(status_suspension))
        self.created_at = self.validate_and_set_created_at(created_at)

    def to_dict(self):
        return {
            'user_id': self.suspension_id,
            'suspension_id': self.suspension_id,
            'date_suspension': self.date_suspencion,
            'date_reactivation': self.date_reactivation,
            'reason': self.reason,
            'created_at': self.created_at,
            'status_suspension': self.status.value
        }

    @staticmethod
    def validade_and_set_suspension_id(suspension_id: str) -> str:
        if not suspension_id:
            raise InvalidParameter('suspension_id', 'is required')
        if not isinstance(suspension_id, str):
            raise InvalidParameter('suspension_id', 'must be a str')
        return suspension_id

    @staticmethod
    def validate_and_set_date_suspencion(date_suspension: int) -> int:
        if not date_suspension:
            raise InvalidParameter('date_suspension', 'is required')
        if not isinstance(date_suspension, int):
            raise InvalidParameter('date_suspension', 'must be a int')
        return date_suspension

    @staticmethod
    def validate_and_set_date_reactivation(date_reactivation: int or None) -> int or None:
        if not date_reactivation:
            return None
        if not isinstance(date_reactivation, int):
            raise InvalidParameter('date_reactivation', 'must be a int')
        return date_reactivation

    @staticmethod
    def validate_and_set_reason(reason: str) -> str:
        if not reason:
            raise InvalidParameter('Justificativa', 'é obrigatória')
        if not isinstance(reason, str):
            raise InvalidParameter('reason', 'must be a str')
        return reason

    @staticmethod
    def validate_and_set_status_suspension(status: STATUS_SUSPENSION_ENUM) -> STATUS_SUSPENSION_ENUM:
        if not status:
            raise InvalidParameter('status', 'is required')
        if not isinstance(status, STATUS_SUSPENSION_ENUM):
            raise InvalidParameter('status', 'must be a STATUS_SUSPENSION_ENUM')
        return status

    @staticmethod
    def validate_and_set_created_at(created_at: int) -> int:
        if not created_at:
            raise InvalidParameter('created_at', 'is required')
        if not isinstance(created_at, int):
            raise InvalidParameter('created_at', 'must be a int')
        return created_at
