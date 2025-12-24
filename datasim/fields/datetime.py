import random
from datetime import date, datetime, timedelta
import pytz

from .base import Field


class Date(Field):
    def __init__(self, start, end, *, func=None):
        super().__init__(func)

        self.start = self._parse_date(start)
        self.end = self._parse_date(end)

        if self.start > self.end:
            raise ValueError("start must be <= end")

        self._delta_days = (self.end - self.start).days

    @staticmethod
    def _parse_date(value) -> date:
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            return date.fromisoformat(value)
        raise TypeError("Date must be date or ISO string")

    def base_generation(self, context=None) -> date:
        offset = random.randint(0, self._delta_days)
        return self.start + timedelta(days=offset)


class DateTime(Field):
    def __init__(self, start, end, *, tz = None, func=None):
        super().__init__(func)

        self.start = self._parse_datetime(start)
        self.end = self._parse_datetime(end)

        if self.start > self.end:
            raise ValueError("start must be <= end")

        self._delta_seconds = int((self.end - self.start).total_seconds())

        if tz:
            try:
                self.tzinfo = pytz.timezone(tz)
            except Exception as e:
                raise ValueError(f"Invalid timezone '{tz}': {e}")
        else:
            self.tzinfo = None

    @staticmethod
    def _parse_datetime(value) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        raise TypeError("DateTime must be datetime or ISO string")

    def base_generation(self, context=None) -> datetime:
        offset_seconds = random.randint(0, self._delta_seconds)
        dt = self.start + timedelta(seconds=offset_seconds)

        if self.tzinfo:
            if dt.tzinfo is None:
                dt = pytz.UTC.localize(dt)
            dt = dt.astimezone(self.tzinfo)

        return dt