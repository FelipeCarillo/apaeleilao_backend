import json
from typing import Any


class HttpResponse:
    def __init__(self, status_code: int, body: Any):
        self.__status_code = status_code
        self.__body = body

    @property
    def status_code(self):
        return self.__status_code

    @property
    def body(self):
        return self.__body

    @property
    def data(self):
        return {'statusCode': self.status_code,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(self.body)}


class OK(HttpResponse):
    def __init__(self, body: Any):
        super().__init__(status_code=200, body=body)


class Created(HttpResponse):
    def __init__(self, body: Any):
        super().__init__(status_code=201, body=body)


class BadRequest(HttpResponse):
    def __init__(self, body: Any):
        super().__init__(status_code=400, body=body)


class Unauthorized(HttpResponse):
    def __init__(self, body: Any):
        super().__init__(status_code=401, body=body)


class Forbidden(HttpResponse):
    def __init__(self, body: Any):
        super().__init__(status_code=403, body=body)


class NotFound(HttpResponse):
    def __init__(self, body: Any):
        super().__init__(status_code=404, body=body)


class NoContent(HttpResponse):
    def __init__(self, body: Any):
        super().__init__(status_code=204, body=body)


class InternalServerError(HttpResponse):
    def __init__(self, body: Any):
        super().__init__(status_code=500, body=body)
