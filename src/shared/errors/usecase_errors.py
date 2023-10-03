from src.shared.errors.main_error import MainError


class DataAlreadyUsed(MainError):
    def __init__(self, body: str):
        super().__init__(f"Parameter {body} already used.")
