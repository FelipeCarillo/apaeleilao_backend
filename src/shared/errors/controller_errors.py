from src.shared.errors.main_error import MainError


class InvalidRequest(MainError):
    def __init__(self):
        super().__init__(f"No request found.")


class InvalidParameter(MainError):
    def __init__(self, parameter: str, body: str):
        super().__init__(f"Invalid {parameter} parameter: {body}")


class MissingParameter(MainError):
    def __init__(self, body: str):
        super().__init__(f"Missing {body} parameter.")


class UserNotAuthenticated(MainError):
    def __init__(self):
        super().__init__(f"User not authenticated.")
