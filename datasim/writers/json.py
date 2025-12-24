import json
from datetime import datetime, date

from .base import Writer


class _DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


class JSONWriter(Writer):
    def write(self, path, rows):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                rows,
                f,
                ensure_ascii=False,
                indent=4,
                cls=_DateTimeEncoder
            )