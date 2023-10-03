from src.shared.errors.main_error import MainError


class InvalidRequest(MainError):
    def __init__(self):
        super().__init__(f"No request found.")


class MissingParameter(MainError):
    def __init__(self, body: str):
        super().__init__(f"Missing {body} parameter.")
