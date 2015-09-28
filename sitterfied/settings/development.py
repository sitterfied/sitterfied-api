# -*- coding: utf-8 -*-
from celery.schedules import crontab
from kombu import Exchange, Queue

from .base import *

DEBUG = TEMPLATE_DEBUG = True

SESSION_COOKIE_NAME = 'sitterfied-dev'

INTERNAL_IPS = (
    '::1',
    '127.0.0.1',
    '192.168.100.1',
)

# ShortUrl Redis Configuration
REDIS_URL = 'redis://127.0.0.1:6379'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sitterfied',
        'USER': 'vagrant',
        'PASSWORD': 'vagrant',
        'HOST': 'localhost',
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
    },
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = PROJECT_ROOT.child("media")
MEDIA_URL = "/media/"

STATIC_ROOT = "/www/static"

GOOGLE_OAUTH_CLIENT_ID = '213296649304-10d5ppglkmjmq7l60uub4r5nvnklfjoa.apps.googleusercontent.com'
GOOGLE_OAUTH_CLIENT_SECRET = 'u9BePfC9OC9Z3XkO0SMJbwkq'
GOOGLE_OAUTH_REDIRECT_URI = "http://sitterfied.ngrok.com"

# Override Short URL
SHORT_URL = 'localhost:8000/'

# Override Facebook App ID
FACEBOOK_APP_ID = '746551758706532'

# Celery configuration
BROKER_URL = REDIS_URL + '/1'
CELERY_DEFAULT_QUEUE = 'sitterfied-dev'
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
}

# Override Job Reminder Times
FAST_SEND_REMINDERS = True
JOB_FIRST_REMINDER = 60
JOB_RELIEF_REMINDER = 180
JOB_SECOND_REMINDER = 120

FACEBOOK_APP_ID = '624946094225118'

GOOGLE_OAUTH_CLIENT_ID = '305141264963-9gamu3g0ja74ch7pcssmmk75shtk9ftc.apps.googleusercontent.com'
GOOGLE_OAUTH_CLIENT_SECRET = 'LSeO2JmrERhe_vRNUFnVsfuc'
GOOGLE_OAUTH_REDIRECT_URI = 'https://test.sitterfied.com'

HELLOBAR_APP_ID = 'e12e8fdf8d04502e0b6c4b41379e97f917b64d65'

INTERCOM_APP_ID = 'a9ac72f2db462866c33f72e70463f02f08423b4a'
INTERCOM_API_SECRET = 'nBuKwWJXM-BdRNebRRFzMTEwUq9Me4XwHjeuZjpx'

KNOWTIFY_API_TOKEN = '4a866b43f5f0f148d62fb8fcdf668d6f'

MANDRILL_API_KEY = 'eSmAHcO6VEK6DaZPoj12xA'

SEGMENT_API_KEY = 'NMTOJEsFZj98UT5vWkJ9HET5bhE2Z04N'

TWILIO_ACCOUNT_SID = "AC08f154853d531705433b3ad705bff51a"
TWILIO_AUTH_TOKEN = "70edab4584f7dba5b65af0061d999b88"
TWILIO_DEFAULT_CALLERID = "+19088384816"

UPLOADCARE = {
    'pub_key': '2ca29096885dea0df2a4',
    'secret': '9ccdafc98ed97c35380d',
    'upload_base_url': 'https://ucarecdn.com/',
}
