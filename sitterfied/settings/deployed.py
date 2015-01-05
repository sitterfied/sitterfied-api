# -*- coding: utf-8 -*-
from .base import *
from .mandrill import *

from celery.schedules import crontab
from urllib import quote_plus

DEBUG = False

# AWS Settings
AWS_REGION = 'us-east-1'
AWS_ACCESS_KEY_ID = 'AKIAIRC5KBNUD4ERCW5A'
AWS_SECRET_ACCESS_KEY = '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'

MIDDLEWARE_CLASSES += (
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
)

# Celery Configuration
BROKER_TRANSPORT_OPTIONS = {'region': AWS_REGION}
DEFAULT_TASK_LOCK_EXPIRE = 60 * 5
BROKER_URL = 'sqs://{}:{}@'.format(AWS_ACCESS_KEY_ID, quote_plus(AWS_SECRET_ACCESS_KEY))

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
    }
}

try:
    JOB_FIRST_REMINDER = int(env.get('JOB_FIRST_REMINDER'))
    JOB_SECOND_REMINDER = int(env.get('JOB_SECOND_REMINDER'))
    JOB_RELIEF_REMINDER = int(env.get('JOB_RELIEF_REMINDER'))
except:
    pass