import re
from abc import ABC
from typing import List, Optional
from src.shared.errors.entities_errors import UserEntityError
from src.shared.errors.controller_errors import MissingParameter, InvalidParameter
from src.shared.structure.entities.suspension import Suspension
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM


class User(ABC):
    user_id: str
    first_name: str
    last_name: str
    cpf: str
    email: str
    phone: str
    password: str
    accepted_terms: bool
    status_account: STATUS_USER_ACCOUNT_ENUM
    suspensions: List[Optional[Suspension]]
    date_joined: int
    verification_code: str
    verification_code_expires_at: int
    password_reset_code: str
    password_reset_code_expires_at: int
    USER_ID_LENGTH = 36
    NAME_MIN_LENGTH = 2
    NAME_MAX_LENGTH = 255

    def __init__(self, user_id: str = None, first_name: str = None, last_name: str = None, cpf: str = None,
                 email: str = None, phone: str = None, password: str = None, accepted_terms: bool = None,
                 status_account: STATUS_USER_ACCOUNT_ENUM = None, suspensions: List[Optional[Suspension]] = None,
                 date_joined: int = None, verification_code: int = None, verification_code_expires_at: int = None,
                 password_reset_code: int = None, password_reset_code_expires_at: int = None):

        self.user_id = self.validate_and_set_user_id(user_id)
        self.first_name = self.validate_and_set_first_name(first_name)
        self.last_name = self.validate_and_set_last_name(last_name)
        self.cpf = self.validate_and_set_cpf(cpf)
        self.email = self.validate_and_set_email(email)
        self.phone = self.validate_and_set_phone(phone)
        self.password = self.validate_and_set_password(password)
        self.accepted_terms = self.validate_and_set_accepted_terms(accepted_terms)
        self.status_account = self.validate_and_set_status_account(status_account)
        self.suspensions = self.validate_and_set_suspensions(suspensions)
        self.date_joined = self.validate_and_set_date_joined(date_joined)
        self.verification_code = self.validate_and_set_verification_code(verification_code)
        self.verification_code_expires_at = self.validate_and_set_verification_code_expires_at(
            verification_code_expires_at)
        self.password_reset_code = self.validate_and_set_password_reset_code(password_reset_code)
        self.password_reset_code_expires_at = self.validate_and_set_password_reset_code_expires_at(
            password_reset_code_expires_at)

    def to_dict(self):
        for index, item in enumerate(self.suspensions):
            if item is not None:
                self.suspensions[index] = item.to_dict()

        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'cpf': self.cpf,
            'email': self.email,
            'phone': self.phone,
            'password': self.password,
            'accepted_terms': self.accepted_terms,
            'status_account': self.status_account,
            'suspensions': self.suspensions,
            'date_joined': self.date_joined,
            'verification_code': self.verification_code,
            'verification_code_expires_at': self.verification_code_expires_at,
            'password_reset_code': self.password_reset_code,
            'password_reset_code_expires_at': self.password_reset_code_expires_at,
        }

    @staticmethod
    def validate_and_set_user_id(user_id: str) -> str or None:
        if user_id is None: raise MissingParameter("user_id")
        if type(user_id) != str: raise InvalidParameter("user_id", "deve ser str.")
        if len(user_id) != User.USER_ID_LENGTH: raise InvalidParameter("user_id", "deve ter 36 caracteres.")
        return user_id

    @staticmethod
    def validate_and_set_first_name(first_name: str) -> str or None:
        if first_name is None: raise MissingParameter("first_name")
        if User.NAME_MIN_LENGTH < len(first_name) >= User.NAME_MAX_LENGTH: raise InvalidParameter(
            "first_name", "deve ter no mínimo 2 caracteres e no máximo 255.")
        if type(first_name) != str: raise InvalidParameter("first_name", "deve ser str.")
        return first_name

    @staticmethod
    def validate_and_set_last_name(last_name: str) -> str or None:
        if last_name is None: raise MissingParameter("last_name")
        if type(last_name) != str: raise InvalidParameter("last_name", "deve ser str.")
        if User.NAME_MIN_LENGTH < len(last_name) >= User.NAME_MAX_LENGTH: raise InvalidParameter(
            "last_name", "deve ter no mínimo 2 caracteres e no máximo 255.")
        return last_name

    @staticmethod
    def validate_and_set_cpf(cpf: str) -> str or None:
        if cpf is None: raise MissingParameter("cpf")
        if type(cpf) != str: raise InvalidParameter("cpf", "deve ser str.")
        if not cpf.isnumeric():
            raise InvalidParameter("cpf", "deve ser numérico.")
        cpf = cpf.replace(".", "").replace("-", "").replace(" ", "")
        if len(cpf) != 11: raise InvalidParameter("cpf", "deve ter 11 caracteres.")
        return cpf

    @staticmethod
    def validate_and_set_email(email: str) -> str or None:
        if email is None: raise MissingParameter("email")
        if re.fullmatch(r"[A-Za-z0-9_.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email) is None:
            raise InvalidParameter("email", "inválido.")
        if type(email) != str: raise InvalidParameter("email", "deve ser str.")
        return email

    @staticmethod
    def validate_and_set_phone(phone: str) -> str or None:
        if phone is None: raise MissingParameter("phone")
        if type(phone) != str: raise InvalidParameter("phone", "deve ser str.")
        return phone

    @staticmethod
    def validate_and_set_password(password: str) -> str or None:
        if password is None: raise MissingParameter("password")
        if type(password) != str: raise InvalidParameter("password", "deve ser str.")
        return password

    @staticmethod
    def validate_and_set_accepted_terms(accepted_terms: bool) -> bool or None:
        if accepted_terms is None: return None
        if type(accepted_terms) != bool: raise InvalidParameter("accepted_terms", "deve ser bool.")
        return accepted_terms

    @staticmethod
    def validate_and_set_date_joined(date_joined: int) -> int or None:
        if date_joined is None: return None
        if type(date_joined) != int: raise InvalidParameter("date_joined", "deve ser int.")
        return date_joined

    @staticmethod
    def validate_and_set_status_account(status_account: STATUS_USER_ACCOUNT_ENUM):
        if status_account is None: raise MissingParameter("status_account")
        if type(status_account) != STATUS_USER_ACCOUNT_ENUM: raise InvalidParameter("status_account",
                                                                                    "deve ser STATUS_USER_ACCOUNT_ENUM.")
        return status_account

    @staticmethod
    def validate_and_set_suspensions(suspensions: List[Optional[Suspension]]):
        if suspensions is None: raise MissingParameter("suspensions")
        for item in suspensions:
            if type(item) != Suspension and len(suspensions) > 0:
                raise InvalidParameter("suspensions", "deve ser Suspension.")
        return suspensions

    @staticmethod
    def validate_and_set_verification_code(verification_code: int) -> int or None:
        if verification_code is None: return None
        if type(verification_code) != int: raise UserEntityError("verification_code deve ser str.")
        return verification_code

    @staticmethod
    def validate_and_set_verification_code_expires_at(verification_code_expires_at: int) -> int or None:
        if verification_code_expires_at is None: return None
        if type(verification_code_expires_at) != int: raise UserEntityError("verification_code_expires_at deve ser "
                                                                            "time.")
        return verification_code_expires_at

    @staticmethod
    def validate_and_set_password_reset_code(password_reset_code: int) -> int or None:
        if password_reset_code is None: return None
        if type(password_reset_code) != int: raise UserEntityError("password_reset_code deve ser str.")
        return password_reset_code

    @staticmethod
    def validate_and_set_password_reset_code_expires_at(password_reset_code_expires_at: int) -> int or None:
        if password_reset_code_expires_at is None: return None
        if type(password_reset_code_expires_at) != int: raise InvalidParameter("password_reset_code_expires_at deve "
                                                                               "ser time.")
        return password_reset_code_expires_at
