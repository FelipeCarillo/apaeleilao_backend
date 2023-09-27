from main_error import MainError


class EmailAlreadyUsed(MainError):
    def __init__(self):
        super().__init__("Email already used.")


class CPFAlreadyUsed(MainError):
    def __init__(self):
        super().__init__("CPF already used.")


class UserIDAlreadyUsed(MainError):
    def __init__(self):
        super().__init__("User ID already used.")