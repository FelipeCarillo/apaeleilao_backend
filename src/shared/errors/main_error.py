
class MainError:
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return {
            "status_code": self.status_code,
            "message": self.message,
        }