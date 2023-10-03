class MainError(Exception):
    def __init__(self, body: str):
        self.body: str = body
        super().__init__(body)
