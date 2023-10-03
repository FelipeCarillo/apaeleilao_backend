class MainError(Exception):
    def __init__(self, body: str):
        self.__body: str = body
        super().__init__(body)

    @property
    def body(self):
        return self.__body
