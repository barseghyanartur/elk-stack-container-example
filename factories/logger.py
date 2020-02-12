import os
from logging import config, getLogger

__author__ = 'Artur Barseghyan'
__copyright__ = '2020 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'LOGGER',
)

LOGS_DIR_NAME = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)s '
                      '%(thread)s %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
        # This is going to be used for Elasticsearch/Logstash
        'json': {
            'format': '{"date": "%(asctime)s.%(msecs)03d",'
                      ' "id": "%(id)s",'
                      ' "success": "%(success)s",'
                      ' "action": "%(message)s"}',
            'datefmt': "%Y-%m-%dT%H:%M:%S",  # Elasticsearch datetime format
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR_NAME, "file.log"),
            'maxBytes': 1048576,
            'backupCount': 99,
            'formatter': 'verbose',
        },
        'json': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR_NAME, "json.log"),
            'maxBytes': 1048576,
            'backupCount': 99,
            'formatter': 'json',
        },
    },
    'loggers': {
        'example': {
            'handlers': ['json'],
            'propagate': False,
        },
    },
}

config.dictConfig(LOGGING_CONFIG)

LOGGER = getLogger('example')
