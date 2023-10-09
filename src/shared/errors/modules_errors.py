from src.shared.errors.main_error import MainError


class InvalidRequest(MainError):
    def __init__(self):
        super().__init__(f"No request found.")


class InvalidParameter(MainError):
    def __init__(self, parameter: str, body: str):
        super().__init__(f"{parameter} {body}.")


class MissingParameter(MainError):
    def __init__(self, body: str):
        super().__init__(f"{body} está faltando.")


class DataAlreadyUsed(MainError):
    def __init__(self, message: str):
        super().__init__(f"{message} está em uso.")


class UserNotAuthenticated(MainError):
    def __init__(self, message: str = None):
        if message:
            super().__init__(message)
        else:
            super().__init__(f"Usuário não autenticado.")
