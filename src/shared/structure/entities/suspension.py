from src.shared.errors.entities_errors import SuspensionEntityError
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
            raise SuspensionEntityError('suspension_id is required.')
        if not isinstance(suspension_id, str):
            raise SuspensionEntityError('suspension_id must be a str.')
        return suspension_id

    @staticmethod
    def validate_and_set_date_suspencion(date_suspencion: int) -> int:
        if not date_suspencion:
            raise SuspensionEntityError('date_suspension is required.')
        if not isinstance(date_suspencion, int):
            raise SuspensionEntityError('date_suspension must be a int.')
        return date_suspencion

    @staticmethod
    def validate_and_set_date_reactivation(date_reactivation: int) -> int:
        if not date_reactivation:
            raise SuspensionEntityError('date_reactivation is required.')
        if not isinstance(date_reactivation, int):
            raise SuspensionEntityError('date_reactivation must be a int.')
        return date_reactivation

    @staticmethod
    def validate_and_set_reason(reason: str) -> str:
        if not reason:
            raise SuspensionEntityError('reason is required.')
        if not isinstance(reason, str):
            raise SuspensionEntityError('reason must be a str.')
        return reason

    @staticmethod
    def validate_and_set_status(status: STATUS_SUSPENSION_ENUM) -> STATUS_SUSPENSION_ENUM:
        if not status:
            raise SuspensionEntityError('status is required.')
        if not isinstance(status, STATUS_SUSPENSION_ENUM):
            raise SuspensionEntityError('status must be a STATUS_SUSPENSION_ENUM.')
        return status
