from src.shared.errors.modules_errors import InvalidParameter
from src.shared.structure.enums.suspension_enum import STATUS_SUSPENSION_ENUM


class Suspension:
    suspension_id: str
    date_suspencion: int
    date_reactivation: int
    reason: str
    status: STATUS_SUSPENSION_ENUM

    def __init__(self, suspension_id: str = None, date_suspencion: int = None, date_reactivation: int = None,
                 reason: str = None, status: STATUS_SUSPENSION_ENUM = None):
        self.suspension_id = self.validade_and_set_suspension_id(suspension_id)
        self.date_suspencion = self.validate_and_set_date_suspencion(date_suspencion)
        self.date_reactivation = self.validate_and_set_date_reactivation(date_reactivation)
        self.reason = self.validate_and_set_reason(reason)
        self.status = self.validate_and_set_status(status)

    def to_dict(self):
        return {
            'user_id': self.suspension_id,
            'date_suspencion': self.date_suspencion,
            'date_reactivation': self.date_reactivation,
            'reason': self.reason,
            'status': self.status
        }

    @staticmethod
    def validade_and_set_suspension_id(suspension_id: str) -> str:
        if not suspension_id:
            raise InvalidParameter('suspension_id', 'is required.')
        if not isinstance(suspension_id, str):
            raise InvalidParameter('suspension_id', 'must be a str.')
        return suspension_id

    @staticmethod
    def validate_and_set_date_suspencion(date_suspencion: int) -> int:
        if not date_suspencion:
            raise InvalidParameter('date_suspencion', 'is required.')
        if not isinstance(date_suspencion, int):
            raise InvalidParameter('date_suspencion', 'must be a int.')
        return date_suspencion

    @staticmethod
    def validate_and_set_date_reactivation(date_reactivation: int) -> int:
        if not date_reactivation:
            raise InvalidParameter('date_reactivation', 'is required.')
        if not isinstance(date_reactivation, int):
            raise InvalidParameter('date_reactivation', 'must be a int.')
        return date_reactivation

    @staticmethod
    def validate_and_set_reason(reason: str) -> str:
        if not reason:
            raise InvalidParameter('Justificativa', 'é obrigatória.')
        if not isinstance(reason, str):
            raise InvalidParameter('reason', 'must be a str.')
        return reason

    @staticmethod
    def validate_and_set_status(status: STATUS_SUSPENSION_ENUM) -> STATUS_SUSPENSION_ENUM:
        if not status:
            raise InvalidParameter('status is required.')
        if not isinstance(status, STATUS_SUSPENSION_ENUM):
            raise InvalidParameter('status must be a STATUS_SUSPENSION_ENUM.')
        return status
