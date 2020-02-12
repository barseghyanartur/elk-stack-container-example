import logging
import json
from typing import List

__author__ = 'Artur Barseghyan'
__copyright__ = '2020 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'JsonFormatter',
)


class JsonFormatter(logging.Formatter):
    def __init__(self, keys: List[str]):
        """A custom Formatter that formats a LogRecord as JSON

        :param keys: list with whitelisted keys to log
        """
        if keys:
            self.keys = keys
        else:
            self.keys = [ 'asctime', 'name', 'levelname', 'message']

        super().__init__()

    def format(self, record) -> str:
        """Formats the LogRecord as JSON

        :param record: a LogRecord
        :return: string
        """
        data = {
            key: getattr(record, key, None) for key in self.keys
        }
        return json.dumps(data)
