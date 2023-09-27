import re
import datetime
from abc import ABC
from ...errors.entities_errors import UserEntityError


class User(ABC):
    user_id: str  # required and unique
    first_name: str
    last_name: str
    cpf: str
    phone: str
    password: str  # required
    accepted_terms: bool
    is_active: bool
    date_joined: int
    is_verified: bool
    verification_code: str
    verification_code_expires_at: int
    password_reset_code: str
    password_reset_code_expires_at: int
    USER_ID_LENGTH = 36
    NAME_MIN_LENGTH = 2
    NAME_MAX_LENGTH = 255

    def __init__(self, user_id: str = None, first_name: str = None, last_name: str = None, cpf: str = None,
                 email: str = None, phone: str = None, password: str = None,
                 accepted_terms: bool = None, date_joined: int = None, is_verified: bool = None,
                 verification_code: int = None, verification_code_expires_at: int = None,
                 password_reset_code: int = None, password_reset_code_expires_at: int = None):

        self.user_id = self.validate_and_set_user_id(user_id)
        self.first_name = self.validate_and_set_first_name(first_name)
        self.last_name = self.validate_and_set_last_name(last_name)
        self.cpf = self.validate_and_set_cpf(cpf)
        self.email = self.validate_and_set_email(email)
        self.phone = self.validate_and_set_phone(phone)
        self.password = self.validate_and_set_password(password)
        self.accepted_terms = self.validate_and_set_accepted_terms(accepted_terms)
        self.date_joined = self.validate_and_set_date_joined(date_joined)
        self.is_verified = self.validate_and_set_is_verified(is_verified)
        self.verification_code = self.validate_and_set_verification_code(verification_code)
        self.verification_code_expires_at = self.validate_and_set_verification_code_expires_at(
            verification_code_expires_at)
        self.password_reset_code = self.validate_and_set_password_reset_code(password_reset_code)
        self.password_reset_code_expires_at = self.validate_and_set_password_reset_code_expires_at(
            password_reset_code_expires_at)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'cpf': self.cpf,
            'email': self.email,
            'phone': self.phone,
            'password': self.password,
            'accepted_terms': self.accepted_terms,
            'date_joined': self.date_joined,
            'is_verified': self.is_verified,
            'verification_code': self.verification_code,
            'verification_code_expires_at': self.verification_code_expires_at,
            'password_reset_code': self.password_reset_code,
            'password_reset_code_expires_at': self.password_reset_code_expires_at,
        }

    @staticmethod
    def validate_and_set_user_id(user_id: str) -> str or None:
        if user_id is None: raise UserEntityError("user_id não pode ser nulo.")
        if type(user_id) != str: raise UserEntityError("user_id deve ser str.")
        if len(user_id) != User.USER_ID_LENGTH: raise UserEntityError("user_id deve ter 36 caracteres.")
        return user_id

    @staticmethod
    def validate_and_set_first_name(first_name: str) -> str or None:
        if first_name is None: raise UserEntityError("first_name não pode ser nulo.")
        if User.NAME_MIN_LENGTH < len(first_name) >= User.NAME_MAX_LENGTH: raise UserEntityError(
            "first_name deve ter no mínimo 2 caracteres e no máximo 255.")
        if type(first_name) != str: raise UserEntityError("first_name deve ser str.")
        return first_name

    @staticmethod
    def validate_and_set_last_name(last_name: str) -> str or None:
        if last_name is None: raise UserEntityError("last_name não pode ser nulo.")
        if type(last_name) != str: raise UserEntityError("last_name deve ser str.")
        if User.NAME_MIN_LENGTH < len(last_name) >= User.NAME_MAX_LENGTH: raise UserEntityError(
            "last_name deve ter no mínimo 2 caracteres e no máximo 255.")
        return last_name

    @staticmethod
    def validate_and_set_cpf(cpf: str) -> str or None:
        if cpf is None: raise UserEntityError("cpf não pode ser nulo.")
        cpf = cpf.replace(".", "").replace("-", "").replace(" ", "")
        if not cpf.isnumeric(): raise UserEntityError("cpf deve ser numérico.")
        if type(cpf) != str: raise UserEntityError("cpf deve ser str.")
        if len(cpf) != 11: raise UserEntityError("cpf deve ter 11 caracteres.")
        return cpf

    @staticmethod
    def validate_and_set_email(email: str) -> str or None:
        if email is None: raise UserEntityError("email não pode ser nulo.")
        if re.fullmatch(r"[A-Za-z0-9_.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email) is None:
            raise UserEntityError("email inválido.")
        if type(email) != str: raise UserEntityError("email deve ser str.")
        return email

    @staticmethod
    def validate_and_set_phone(phone: str) -> str or None:
        if phone is None: raise UserEntityError("phone não pode ser nulo.")
        if type(phone) != str: raise UserEntityError("phone deve ser str.")
        return phone

    @staticmethod
    def validate_and_set_password(password: str) -> str or None:
        if password is None: raise UserEntityError("password não pode ser nulo.")
        if type(password) != str: raise UserEntityError("password deve ser str.")
        return password

    @staticmethod
    def validate_and_set_accepted_terms(accepted_terms: bool) -> bool or None:
        if accepted_terms is None: return None
        if type(accepted_terms) != bool: raise UserEntityError("accepted_terms deve ser bool.")
        return accepted_terms

    @staticmethod
    def validate_and_set_date_joined(date_joined: int) -> int or None:
        if date_joined is None: return None
        if type(date_joined) != int: raise UserEntityError("date_joined deve ser int.")
        return date_joined

    @staticmethod
    def validate_and_set_is_verified(is_verified: bool) -> bool or None:
        if is_verified is None: return None
        if type(is_verified) != bool: raise UserEntityError("is_verified deve ser bool.")
        return is_verified

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
        if type(password_reset_code_expires_at) != int: raise UserEntityError("password_reset_code_expires_at deve "
                                                                              "ser time.")
        return password_reset_code_expires_at
