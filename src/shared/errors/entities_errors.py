
class UserEntityError(ValueError):
    def __init__(self, message):
        super().__init__(f"User Entity Error: {message}")
