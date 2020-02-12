import logging
import json
from typing import List, Dict, Callable

__author__ = 'Artur Barseghyan'
__copyright__ = '2020 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'JsonFormatter',
)


class JsonFormatter(logging.Formatter):

    def __init__(self, 
                 keys: List[str], 
                 rename: Dict[str, str] = None, 
                 transform: Callable = None, 
                 *args, 
                 **kwargs):
        """A custom Formatter that formats a LogRecord as JSON.

        :param keys: list with whitelisted keys to log.
        """
        if keys:
            self.keys = keys
        else:
            self.keys = ['asctime', 'name', 'levelname', 'message']
        if rename:
            self.rename = rename
        else:
            self.rename = {}
        if transform:
            self.transform = transform
        else:
            self.transform = {}
        super().__init__(*args, **kwargs)

    def format(self, record) -> str:
        """Formats the LogRecord as JSON.

        :param record: a LogRecord
        :return: string
        """
        data = {}
        for key in self.keys:
            _key = self.rename.get(key, key)
            _transform = self.transform.get(key)
            if _transform:
                _value = _transform(record)
            else:
                _value = getattr(record, key, None)
            data.update({_key: _value})
        return json.dumps(data)
