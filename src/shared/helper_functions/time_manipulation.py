import time


class TimeManipulation:
    @staticmethod
    def get_current_time() -> int:
        return int(time.time() - 3 * 3600)

    @staticmethod
    def plus_hour(time_now: int, hours: int) -> int:
        return time_now + hours * 3600

    @staticmethod
    def plus_day(time_now: int, days: int) -> int:
        return time_now + days * 24 * 3600
