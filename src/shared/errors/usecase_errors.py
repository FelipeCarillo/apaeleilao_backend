from src.shared.errors.main_error import MainError


class DataAlreadyUsed(MainError):
    def __init__(self, data: list):
        super().__init__(f"{data}")

class UserIDAlreadyUsed(MainError):
    def __init__(self):
        super().__init__("User ID already used.")