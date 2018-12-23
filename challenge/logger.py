import os
import logging

from .settings import BASE_DIR
from .settings import DEBUG

# the basic logger other apps can import
log = logging.getLogger(__name__)

# the minimum reported level
if DEBUG:
    min_level = 'DEBUG'
else:
    min_level = 'INFO'

min_django_level = 'INFO'

# logging dictConfig configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'timestampthread': {
            'format': "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [%(name)-20.20s]  %(message)s",
        },
    },
    'handlers': {
        'logfile': {
            'level': min_level,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logfile'),
            'maxBytes': 50 * 10**6,
            'backupCount': 3,
            'formatter': 'timestampthread'
        },
        'console': {
            'level': min_level,
            'class': 'logging.StreamHandler',
            'formatter': 'timestampthread'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['logfile', 'console'],
            'level': min_django_level,
            'propagate': False,
        },
        '': {
            'handlers': ['logfile', 'console'],
            'level': min_level,
        },
    },
}