from typing import Any


class OK:
    def __init__(self, data: Any):
        self.__data = data

    @property
    def data(self):
        return {'statusCode': 200, 'body': self.__data}


class Created:
    def __init__(self, data: Any):
        self.__data = data

    @property
    def data(self):
        return {'statusCode': 201, 'body': self.__data}


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
