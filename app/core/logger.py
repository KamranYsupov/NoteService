import sys
import os
import logging
from datetime import datetime

from loguru import logger

from .config import settings

log_level = settings.log_level.value

if not os.path.exists('logs'):
    os.makedirs('logs')

logger.add(
    'logs/app_{time:YYYY-MM-DD}.log',
    rotation='1 day',
    retention='7 days',
    level=log_level.upper()
)

LOG_FORMAT = '[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s'
LOG_DEFAULT_HANDLERS = [
    'console',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': LOG_FORMAT},
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': '%(levelprefix)s %(client_addr)s - \%(request_line)s\ %(status_code)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': 'INFO',
        },
        'uvicorn.error': {
            'level': 'INFO',
        },
        'uvicorn.access': {
            'handlers': ['access'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'level': log_level,
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}


logging.basicConfig(
    level=log_level.upper(),
    handlers=[logging.StreamHandler(sys.stdout)],
    format=LOG_FORMAT,
)

def log_exception(exc):
    logger.error(f'Обработана ошибка: {exc}')