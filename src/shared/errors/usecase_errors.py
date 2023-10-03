from src.shared.errors.main_error import MainError


class DataAlreadyUsed(MainError):
    def __init__(self):
        super().__init__(f"Parameter already used")
