from main_error import MainError


class UserEntityError(MainError):
    def __init__(self, message):
        super().__init__(f"User Entity Error: {message}")
