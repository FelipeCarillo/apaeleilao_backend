import re
from abc import ABC

from src.shared.errors.modules_errors import MissingParameter, InvalidParameter
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM, TYPE_ACCOUNT_USER_ENUM


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
    type_account: TYPE_ACCOUNT_USER_ENUM
    date_joined: int
    verification_code: str
    verification_code_expires_at: int
    password_reset_code: str
    password_reset_code_expires_at: int

    def __init__(self, user_id: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 cpf: str = None,
                 email: str = None,
                 phone: str = None,
                 password: str = None,
                 accepted_terms: bool = None,
                 status_account: str = None,
                 type_account: str = None,
                 date_joined: int = None,
                 verification_email_code: str = None,
                 verification_email_code_expires_at: int = None,
                 password_reset_code: str = None,
                 password_reset_code_expires_at: int = None):

        self.user_id = UserValidator.validate_and_set_user_id(user_id)
        self.first_name = UserValidator.validate_and_set_first_name(first_name)
        self.last_name = UserValidator.validate_and_set_last_name(last_name)
        self.cpf = UserValidator.validate_and_set_cpf(cpf)
        self.email = UserValidator.validate_and_set_email(email)
        self.phone = UserValidator.validate_and_set_phone(phone)
        self.password = UserValidator.validate_and_set_password(password)
        self.accepted_terms = UserValidator.validate_and_set_accepted_terms(accepted_terms)
        self.status_account = UserValidator.validate_and_set_status_account(STATUS_USER_ACCOUNT_ENUM(status_account))
        self.type_account = UserValidator.validate_and_set_type_account(TYPE_ACCOUNT_USER_ENUM(type_account))
        self.date_joined = UserValidator.validate_and_set_date_joined(date_joined)
        self.verification_email_code = UserValidator.validate_and_set_verification_email_code(verification_email_code)
        self.verification_email_code_expires_at = UserValidator.validate_and_set_verification_email_code_expires_at(
            verification_email_code_expires_at)
        self.password_reset_code = UserValidator.validate_and_set_password_reset_code(password_reset_code)
        self.password_reset_code_expires_at = UserValidator.validate_and_set_password_reset_code_expires_at(
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
            'status_account': self.status_account.value,
            'type_account': self.type_account.value,
            'date_joined': self.date_joined,
            'verification_email_code': self.verification_email_code,
            'verification_email_code_expires_at': self.verification_email_code_expires_at,
            'password_reset_code': self.password_reset_code,
            'password_reset_code_expires_at': self.password_reset_code_expires_at,
        }


class UserModerator(ABC):
    user_id: str
    access_key: str
    first_name: str
    last_name: str
    cpf: str
    password: str
    accepted_terms: bool
    status_account: STATUS_USER_ACCOUNT_ENUM
    type_account: TYPE_ACCOUNT_USER_ENUM
    date_joined: int
    USER_ID_LENGTH = 36
    NAME_MIN_LENGTH = 3
    NAME_MAX_LENGTH = 200
    PERMITTED_TYPE_ACCOUNT = [TYPE_ACCOUNT_USER_ENUM.MODERATOR]

    def __init__(self, user_id: str = None,
                 access_key: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 cpf: str = None,
                 password: str = None,
                 accepted_terms: bool = None,
                 status_account: str = None,
                 type_account: str = None,
                 date_joined: int = None):
        self.user_id = UserValidator.validate_and_set_user_id(user_id)
        self.access_key = UserValidator.validate_and_set_access_key(access_key)
        self.first_name = UserValidator.validate_and_set_first_name(first_name)
        self.last_name = UserValidator.validate_and_set_last_name(last_name)
        self.cpf = UserValidator.validate_and_set_cpf(cpf)
        self.password = UserValidator.validate_and_set_password(password)
        self.accepted_terms = UserValidator.validate_and_set_accepted_terms(accepted_terms)
        self.status_account = UserValidator.validate_and_set_status_account(STATUS_USER_ACCOUNT_ENUM(status_account))
        self.type_account = self.validate_and_set_type_account(TYPE_ACCOUNT_USER_ENUM(type_account))
        self.date_joined = UserValidator.validate_and_set_date_joined(date_joined)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'access_key': self.access_key,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'cpf': self.cpf,
            'password': self.password,
            'accepted_terms': self.accepted_terms,
            'status_account': self.status_account.value,
            'type_account': self.type_account.value,
            'date_joined': self.date_joined,
        }

    @staticmethod
    def validate_and_set_type_account(type_account: TYPE_ACCOUNT_USER_ENUM):
        if type_account is None:
            raise MissingParameter("type_account")
        if type(type_account) != TYPE_ACCOUNT_USER_ENUM:
            raise InvalidParameter("type_account", "deve ser TYPE_ACCOUNT_USER_ENUM")
        if type_account not in UserModerator.PERMITTED_TYPE_ACCOUNT:
            raise InvalidParameter("type_account",
                                   f"deve ser um dos seguintes valores: {UserModerator.PERMITTED_TYPE_ACCOUNT}")
        return type_account


class UserAdmin(ABC):
    user_id: str
    access_key: str
    password: str
    type_account: TYPE_ACCOUNT_USER_ENUM
    PERMITTED_TYPE_ACCOUNT = [TYPE_ACCOUNT_USER_ENUM.ADMIN]

    def __init__(self, user_id: str = None,
                 access_key: str = None,
                 password: str = None,
                 status_account: str = None,
                 type_account: str = None):
        self.user_id = UserValidator.validate_and_set_user_id(user_id)
        self.access_key = UserValidator.validate_and_set_access_key(access_key)
        self.password = UserValidator.validate_and_set_password(password)
        self.status_account = UserValidator.validate_and_set_status_account(STATUS_USER_ACCOUNT_ENUM(status_account))
        self.type_account = self.validate_and_set_type_account(TYPE_ACCOUNT_USER_ENUM(type_account))

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'access_key': self.access_key,
            'password': self.password,
            'status_account': self.status_account.value,
            'type_account': self.type_account.value,
        }

    @staticmethod
    def validate_and_set_type_account(type_account: TYPE_ACCOUNT_USER_ENUM):
        if type_account is None:
            raise MissingParameter("type_account")
        if type(type_account) != TYPE_ACCOUNT_USER_ENUM:
            raise InvalidParameter("type_account", "deve ser TYPE_ACCOUNT_USER_ENUM")
        if type_account not in UserAdmin.PERMITTED_TYPE_ACCOUNT:
            raise InvalidParameter("type_account",
                                   f"deve ser um dos seguintes valores: {UserAdmin.PERMITTED_TYPE_ACCOUNT}")
        return type_account


class UserValidator(ABC):
    USER_ID_LENGTH = 36
    ACCESS_KEY_LENGTH = 12
    NAME_MIN_LENGTH = 3
    NAME_MAX_LENGTH = 200

    @staticmethod
    def validate_and_set_user_id(user_id: str) -> str or None:
        if user_id is None:
            raise MissingParameter("user_id")
        if type(user_id) != str:
            raise InvalidParameter("user_id", "deve ser str")
        if len(user_id) != UserValidator.USER_ID_LENGTH:
            raise InvalidParameter("user_id", "deve ter 36 caracteres")
        return user_id

    @staticmethod
    def validate_and_set_access_key(access_key: str) -> str or None:
        if access_key is None:
            raise MissingParameter("access_key")
        if type(access_key) != str:
            raise InvalidParameter("access_key", "deve ser str")
        if len(access_key) != UserValidator.ACCESS_KEY_LENGTH:
            raise InvalidParameter("access_key", f"deve ter {UserValidator.ACCESS_KEY_LENGTH} caracteres")
        return access_key

    @staticmethod
    def validate_and_set_first_name(first_name: str) -> str or None:
        if first_name is None:
            raise MissingParameter("Nome")
        if UserValidator.NAME_MIN_LENGTH < len(first_name) >= UserValidator.NAME_MAX_LENGTH:
            raise InvalidParameter(
                "first_name",
                f"deve ter no mínimo {UserValidator.NAME_MIN_LENGTH} caracteres e no máximo {UserValidator.NAME_MAX_LENGTH}")
        if type(first_name) != str:
            raise InvalidParameter("first_name", "deve ser str")
        return first_name

    @staticmethod
    def validate_and_set_last_name(last_name: str) -> str or None:
        if last_name is None:
            raise MissingParameter("Sobrenome")
        if type(last_name) != str:
            raise InvalidParameter("last_name", "deve ser str")
        if UserValidator.NAME_MIN_LENGTH < len(last_name) >= UserValidator.NAME_MAX_LENGTH:
            raise InvalidParameter("last_name",
                                   f"deve ter no mínimo {UserValidator.NAME_MIN_LENGTH} caracteres e no máximo {UserValidator.NAME_MAX_LENGTH}")
        return last_name

    @staticmethod
    def validate_and_set_cpf(cpf: str) -> str or None:
        if cpf is None:
            raise MissingParameter("CPF")
        if type(cpf) != str:
            raise InvalidParameter("cpf", "deve ser str")
        if not cpf.isnumeric():
            raise InvalidParameter("cpf", "deve ser numérico")
        cpf = cpf.replace(".", "").replace("-", "").replace(" ", "")
        if len(cpf) != 11:
            raise InvalidParameter("cpf", "deve ter 11 caracteres")

        numbers = [int(digit) for digit in cpf]

        # Validação do primeiro dígito verificador:
        sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            raise InvalidParameter("CPF", "inválido")

        # Validação do segundo dígito verificador:
        sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            raise InvalidParameter("CPF", "inválido")

        return cpf

    @staticmethod
    def validate_and_set_email(email: str) -> str or None:
        if email is None:
            raise MissingParameter("Email")
        if re.fullmatch(r"[A-Za-z0-9_.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email) is None:
            raise InvalidParameter("Email", "inválido")
        if type(email) != str:
            raise InvalidParameter("Email", "deve ser str")
        return email

    @staticmethod
    def validate_and_set_phone(phone: str) -> str or None:
        if phone is None:
            raise MissingParameter("Celular")
        if type(phone) != str:
            raise InvalidParameter("phone", "deve ser str")
        return phone

    @staticmethod
    def validate_and_set_password(password: str) -> str or None:
        if password is None:
            raise MissingParameter("Senha")
        if type(password) != str:
            raise InvalidParameter("password", "deve ser str")
        return password

    @staticmethod
    def validate_and_set_accepted_terms(accepted_terms: bool) -> bool or None:
        if accepted_terms is None:
            return None
        if type(accepted_terms) != bool:
            raise InvalidParameter("accepted_terms", "deve ser bool")
        return accepted_terms

    @staticmethod
    def validate_and_set_date_joined(date_joined: int) -> int or None:
        if date_joined is None:
            return None
        if type(date_joined) != int:
            raise InvalidParameter("date_joined", "deve ser int")
        return date_joined

    @staticmethod
    def validate_and_set_status_account(status_account: STATUS_USER_ACCOUNT_ENUM):
        if status_account is None:
            raise MissingParameter("status_account")
        if type(status_account) != STATUS_USER_ACCOUNT_ENUM:
            raise InvalidParameter("status_account", "deve ser STATUS_USER_ACCOUNT_ENUM")
        return status_account

    @staticmethod
    def validate_and_set_type_account(type_account: TYPE_ACCOUNT_USER_ENUM):
        if type_account is None:
            raise MissingParameter("type_account")
        if type(type_account) != TYPE_ACCOUNT_USER_ENUM:
            raise InvalidParameter("type_account", "deve ser TYPE_ACCOUNT_USER_ENUM")
        if type_account != TYPE_ACCOUNT_USER_ENUM.USER:
            raise InvalidParameter("type_account", "deve ser USER")
        return type_account

    @staticmethod
    def validate_and_set_verification_email_code(verification_email_code: str) -> str or None:
        if verification_email_code is None:
            return None
        if type(verification_email_code) != str:
            raise InvalidParameter("verification_code", "deve ser str")
        return verification_email_code

    @staticmethod
    def validate_and_set_verification_email_code_expires_at(verification_email_code_expires_at: int) -> int or None:
        if verification_email_code_expires_at is None:
            return None
        if type(verification_email_code_expires_at) != int:
            raise InvalidParameter("verification_code_expires_at", "deve ser int")
        return verification_email_code_expires_at

    @staticmethod
    def validate_and_set_password_reset_code(password_reset_code: str) -> str or None:
        if password_reset_code is None:
            return None
        if type(password_reset_code) != str:
            raise InvalidParameter("password_reset_code", "deve ser str")
        return password_reset_code

    @staticmethod
    def validate_and_set_password_reset_code_expires_at(password_reset_code_expires_at: int) -> int or None:
        if password_reset_code_expires_at is None:
            return None
        if type(password_reset_code_expires_at) != int:
            raise InvalidParameter("password_reset_code_expires_at", "deve ser int")
        return password_reset_code_expires_at
