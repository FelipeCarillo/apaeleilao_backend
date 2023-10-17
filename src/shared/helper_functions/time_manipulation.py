import time


class TimeManipulation:
    def __init__(self, time_now: int = None):
        self.__time_now = time_now if time_now else self.get_current_time()

    @staticmethod
    def get_current_time() -> int:
        return int(time.time() - 3 * 3600)

    def plus_hour(self, hours: float or int) -> int:
        return int(self.__time_now + hours * 3600)

    def plus_day(self, days: float or int) -> int:
        return int(self.__time_now + days * 24 * 3600)

    def plus_minute(self, minutes: float or int) -> int:
        return int(self.__time_now + minutes * 60)

    def plus_seconds(self, seconds: float or int) -> int:
        return int(self.__time_now + seconds)
