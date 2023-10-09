import json
from typing import Dict


class HttpRequest:
    def __init__(self, body: Dict or str):
        self.body = body

    def __call__(self):
        if isinstance(self.body, str):
            self.body = json.loads(self.body)
        if isinstance(self.body, dict):
            self.body = self.body
        if "body" not in self.body:
            self.body = {"body": self.body}
        return self.body


class HttpResponse:
    def __init__(self, status_code: int, body: Dict = None):
        self.status_code = status_code
        self.body = body

    def to_dict(self):
        return {
            "statusCode": self.status_code,
            "headers": {
                "Content-Type": "application/json"
            },
            "isBase64Encoded": False,
            "body": json.dumps(self.body)
        }


class OK(HttpResponse):
    def __init__(self, body: Dict = None, message: str = None):
        super().__init__(status_code=200, body={'body': body, 'message': message})


class Created(HttpResponse):
    def __init__(self, body: Dict = None, message: str = None):
        super().__init__(status_code=201, body={'body': body, 'message': message})


class BadRequest(HttpResponse):
    def __init__(self, body: Dict = None, message: str = None):
        super().__init__(status_code=400, body={'body': body, 'message': message})


class Unauthorized(HttpResponse):
    def __init__(self, body: Dict = None, message: str = None):
        super().__init__(status_code=401, body={'body': body, 'message': message})


class Forbidden(HttpResponse):
    def __init__(self, body: Dict = None, message: str = None):
        super().__init__(status_code=403, body={'body': body, 'message': message})


class NotFound(HttpResponse):
    def __init__(self, body: Dict = None, message: str = None):
        super().__init__(status_code=404, body={'body': body, 'message': message})


class NoContent(HttpResponse):
    def __init__(self, body: Dict = None, message: str = None):
        super().__init__(status_code=204, body={'body': body, 'message': message})


class InternalServerError(HttpResponse):
    def __init__(self, body: Dict = None, message: str = None):
        super().__init__(status_code=500, body={'body': body, 'message': message})
