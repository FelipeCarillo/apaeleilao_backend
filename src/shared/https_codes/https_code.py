import json
from typing import Dict


class HttpRequest:
    def __init__(self, auth: Dict = None, body: Dict or str = None):
        self.auth = auth
        self.body = body

    def __call__(self):
        if self.auth:
            if isinstance(self.auth, str):
                self.auth = json.loads(self.auth)
                if self.auth.get('Authorization'):
                    self.auth['Authorization'] = None if self.auth['Authorization'] == 'null' else self.auth['Authorization']
        response = {'auth': self.auth}
        if self.body:
            if isinstance(self.body, str):
                self.body = json.loads(self.body)
            if 'body' in self.body:
                response['body'] = self.body['body']
            else:
                response['body'] = self.body

        return response


class HttpResponse:
    def __init__(self, status_code: int, body: Dict = None):
        self.status_code = status_code
        self.body = body

    def to_dict(self, origin: str = '*'):
        return {
            "statusCode": self.status_code,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': origin,
            },
            "body": json.dumps(self.body),
            'isBase64Encoded': False
        }


class OK(HttpResponse):
    def __init__(self, body: Dict = None, message: str = None):
        super().__init__(status_code=200, body={'body': body, 'message': message})


class Created(HttpResponse):
    def __init__(self, body: Dict = None, message: str = None):
        super().__init__(status_code=201, body={'body': body, 'message': message})


class NoContent(HttpResponse):
    def __init__(self, body: Dict = None, message: str = None):
        super().__init__(status_code=204, body={'body': body, 'message': message})


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


class ParameterError(HttpResponse):
    def __init__(self, body: Dict = None, message: str = None):
        super().__init__(status_code=422, body={'body': body, 'message': message})


class InternalServerError(HttpResponse):
    def __init__(self, body: Dict = None, message: str = None):
        super().__init__(status_code=500, body={'body': body, 'message': message})
