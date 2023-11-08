from src.shared.errors.main_error import MainError


class UserEntityError(MainError):
    def __init__(self, body):
        super().__init__(f"User Entity Error: {body}")


class SuspensionEntityError(MainError):
    def __init__(self, body):
        super().__init__(f"Suspension Entity Error: {body}")
