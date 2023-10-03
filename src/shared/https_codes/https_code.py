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


class OK:
    def __init__(self, data: Any):
        self.__data = data

    @property
    def data(self):
        return {'statusCode': 200,
                'body': self.__data}


class Created:
    def __init__(self, data: Any):
        self.__data = data

    @property
    def data(self):
        return {'statusCode': 201,
                'body': self.__data}


class BadRequest:
    def __init__(self, data: Any):
        self.__data = data

    @property
    def data(self):
        return {'statusCode': 400, 'body': self.__data}


class Unauthorized:
    def __init__(self, data: Any):
        self.__data = data

    @property
    def data(self):
        return {'statusCode': 401, 'body': self.__data}


class Forbidden:
    def __init__(self, data: Any):
        self.__data = data

    @property
    def data(self):
        return {'statusCode': 403, 'body': self.__data}


class NotFound:
    def __init__(self, data: Any):
        self.__data = data

    @property
    def data(self):
        return {'statusCode': 404, 'body': self.__data}


class NoContent:
    def __init__(self, data: Any):
        self.__data = data

    @property
    def data(self):
        return {'statusCode': 204, 'body': self.__data}


class InternalServerError:
    def __init__(self, data: Any):
        self.__data = data

    @property
    def data(self):
        return {'statusCode': 500, 'body': self.__data}
