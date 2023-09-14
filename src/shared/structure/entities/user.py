from abc import ABC
from time import time
import re


class User(ABC):
    user_id: str  # required and unique
    first_name: str
    last_name: str
    cpf: str  # required and unique
    phone: str
    password: str
    accepted_terms: bool
    is_active: bool
    date_joined: time
    is_verified: bool
    verification_code: str
    verification_code_expires_at: time
    password_reset_code: str
    password_reset_code_expires_at: time
    USER_ID_LENGTH = 36
    NAME_MIN_LENGTH = 2
    NAME_MAX_LENGTH = 255

    def __init__(self, user_id: str = None, first_name: str = None, last_name: str = None, cpf: str = None,
                 email: str = None, phone: str = None, password: str = None,
                 accepted_terms: bool = None, is_active: bool = None, date_joined: str = time, is_verified: bool = None,
                 verification_code: str = None, verification_code_expires_at: time = None,
                 password_reset_code: str = None, password_reset_code_expires_at: time = None):

        self.user_id = self.validate_and_set_user_id(user_id)
        self.first_name = self.validate_and_set_first_name(first_name)
        self.last_name = self.validate_and_set_last_name(last_name)
        self.cpf = self.validate_and_set_cpf(cpf)
        self.email = self.validate_and_set_email(email)
        self.phone = phone
        self.password = password
        self.is_active = is_active
        self.date_joined = date_joined
        self.is_verified = is_verified
        self.verification_code = verification_code
        self.verification_code_expires_at = verification_code_expires_at
        self.password_reset_code = password_reset_code
        self.password_reset_code_expires_at = password_reset_code_expires_at

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
        cpf = cpf.replace(".", "").replace("-", "").replace(" ", "")  # remove all special characters
        if cpf is None: raise UserEntityError("cpf não pode ser nulo.")
        if not cpf.isnumeric(): raise UserEntityError("cpf deve ser numérico.")
        if type(cpf) != str: raise UserEntityError("cpf deve ser str.")
        if len(cpf) != 11: raise UserEntityError("cpf deve ter 11 caracteres.")
        return cpf

    @staticmethod
    def validate_and_set_email(email: str) -> str or None:
        if re.fullmatch(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+",
                        email) is None: raise UserEntityError("email inválido.")
        if email is None: raise UserEntityError("email não pode ser nulo.")
        if type(email) != str: raise UserEntityError("email deve ser str.")
        return email

    @staticmethod
    def validate_and_set_phone(phone: str) -> str or None:
        if phone is None: raise UserEntityError("phone não pode ser nulo.")
        if type(phone) != str: raise UserEntityError("phone deve ser str.")
        return phone


class UserEntityError(ValueError):
    def __init__(self, message):
        super().__init__(f"User Entity Error: {message}")
