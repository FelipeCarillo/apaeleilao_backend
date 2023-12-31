import time
import datetime


class TimeManipulation:
    def __init__(self, time_now: int = None, datetime_now: str = None, datetime_format: str = '%Y-%m-%d %H:%M:%S'):
        if time_now:
            self.__time_now = time_now
        if datetime_now:
            self.__time_now = int(datetime.datetime.strptime(datetime_now, datetime_format).timestamp())
        if not time_now and not datetime_now:
            self.__time_now = self.get_current_time()

    @staticmethod
    def get_current_time() -> int:
        return int(time.time() - 3 * 3600)

    def get_time(self) -> int:
        return self.__time_now

    def plus_hour(self, hours: float or int) -> int:
        return int(self.__time_now + hours * 3600)

    def plus_day(self, days: float or int) -> int:
        return int(self.__time_now + days * 24 * 3600)

    def plus_minute(self, minutes: float or int) -> int:
        return int(self.__time_now + minutes * 60)

    def plus_seconds(self, seconds: float or int) -> int:
        return int(self.__time_now + seconds)

    def get_datetime(self, time_now: int = None, datetime_format: str = None) -> str:
        time_now = time_now if time_now else self.__time_now
        datetime_format = datetime_format if datetime_format else '%Y-%m-%d %H:%M:%S'
        return datetime.datetime.fromtimestamp(time_now).strftime(datetime_format)
