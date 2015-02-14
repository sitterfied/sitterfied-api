# -*- coding: utf-8 -*-
# -*- mode: python -*-
from .base import *
from .mandrill import *

from celery.schedules import crontab
from urllib import quote_plus

DEBUG = TEMPLATE_DEBUG = True

# Send Admin emails from the test subdomain
SERVER_EMAIL = 'no-reply@test.sitterfied.com'

SESSION_COOKIE_NAME = 'sitterfied-test'

ELASTICACHE_ENDPOINT = 'website-test.ug6jhv.0001.use1.cache.amazonaws.com:6379'

REDIS_URL = 'redis://{}'.format(ELASTICACHE_ENDPOINT)

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': ELASTICACHE_ENDPOINT,
        'OPTIONS': {
            'DB': 1,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'PICKLE_VERSION': 2,
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sitterfied',
        'USER': 'sitterfied',
        'PASSWORD': '^uM*e3xj79eFLrc',
        'HOST': 'website-test-website-server-database.cd92rfe8vffs.us-east-1.rds.amazonaws.com'
        'PORT': 5432,
    }
}

MIDDLEWARE_CLASSES += (
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
)

# Celery Configuration
BROKER_TRANSPORT_OPTIONS = {
    'region': AWS_REGION,
    'queue_name_prefix': 'test-'
    # Set visibility timeout to 1 year, this is necessary to prevent
    # celery from executing scheduled celery tasks multiple times.
    'visibility_timeout': 43200,

}

BROKER_URL = 'sqs://{}:{}@'.format(AWS_ACCESS_KEY_ID, quote_plus(AWS_SECRET_ACCESS_KEY))

CELERY_DEFAULT_QUEUE = 'sitterfied-test'
CELERY_QUEUES = (
    Queue(CELERY_DEFAULT_QUEUE, Exchange(CELERY_DEFAULT_QUEUE, routing_key=CELERY_DEFAULT_QUEUE)),
)

# Celery Beat Configuration
CELERYBEAT_SCHEDULE = {
    'check-for-completed-jobs': {
        'task': 'sitterfied.app.tasks.jobs.check_for_completed_jobs',
        'schedule': crontab(minute='5'),
    },
    'check-for-canceled-jobs': {
        'task': 'sitterfied.app.tasks.jobs.check_for_canceled_jobs_with_incorrect_status',
        'schedule': crontab(hour='0', minute='15',),
    },
    'mark-expired-jobs': {
        'task': 'sitterfied.app.tasks.jobs.mark_expired_jobs',
        'schedule': crontab(minute='10'),
    },
    'cleanup-stale-sqs-queues': {
        'task': 'sitterfied.utils.tasks.cleanup_stale_sqs_queues',
        'schedule': crontab(hour='*', minute=0, day_of_week='*'),
    },
    'update-knowtify': {
        'task': 'sitterfied.utils.knowtify.update_knowtify',
        'schedule': crontab(hour=22, minute=3, day_of_week='Mon'),
    },
}

"""
# Google OAuth Configuration
GOOGLE_OAUTH_CLIENT_ID = '305141264963-9gamu3g0ja74ch7pcssmmk75shtk9ftc.apps.googleusercontent.com'
GOOGLE_OAUTH_CLIENT_SECRET = 'LSeO2JmrERhe_vRNUFnVsfuc'
GOOGLE_OAUTH_REDIRECT_URI = 'http://test.sitterfied.com'

# Override URL Shortening
SHORT_URL = 'test.sttrfd.us/'

# Override Popcorn Metrics ID
POPCORN_METRICS_ID = '53f62873ed69ca02000003ef'

# Override Twilio Configuration
TWILIO_DEFAULT_CALLERID = '+19088384816'

# Override Facebook App ID
FACEBOOK_APP_ID = '624946094225118'

# Override Sideswipe.io Token
SIDESWIPE_IO_TOKEN = 'd647eccfe96499d0f8aa85a7f96a2cd5'

# Knowtify Config
KNOWTIFY_API_TOKEN = '4a866b43f5f0f148d62fb8fcdf668d6f'

# Override Job Reminder Times
JOB_FIRST_REMINDER = 180  # 3 minutes
JOB_RELIEF_REMINDER = 1680  # 28 minutes
JOB_SECOND_REMINDER = 60  # 1 minute
"""

LOG_LEVEL = 'DEBUG'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'ignore_http_header': {
            '()': 'sitterfied.utils.log.IgnoreRegularExpressionFilter',
            'pattern': r'^Invalid HTTP_HOST header',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': LOG_LEVEL,
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'log_file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/var/log/sitterfied/application.log',
            'maxBytes': 1024 * 1024 * 25,  # 25 MB
            'backupCount': 5,
        },
        'mail_admins': {
            'filters': ['ignore_http_header', 'require_debug_false'],
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'email_backend': 'django_ses.SESBackend',
        },
    },
    'loggers': {
        'boto': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        '': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
