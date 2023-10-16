import time


class TimeManipulation:
    def __init__(self, time_now: int = None):
        self.__time_now = time_now if time_now else self.get_current_time()

    @staticmethod
    def get_current_time() -> int:
        return int(time.time() - 3 * 3600)

    def plus_hour(self, hours: int) -> int:
        return self.__time_now + hours * 3600

    def plus_day(self, days: int) -> int:
        return self.__time_now + days * 24 * 3600
