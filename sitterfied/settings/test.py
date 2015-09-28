# -*- coding: utf-8 -*-
# Must come before imports
ENABLE_FAKE_S3 = True

from .development import *

DEBUG = TEMPLATE_DEBUG = False

# Define custom test runner to control logging level
TEST_RUNNER = 'sitterfied.test.APITestRunner'

# For testing, use sqlite which will run in-memory
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': '/tmp/test'
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Effectively turn off throttling during tests. Surprising there isn't a
# central way to do this.
REST_FRAMEWORK.update({
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'sitterfied.test.FormRenderer',
    ),
})

CELERY_ALWAYS_EAGER = True

DISABLE_SHORT_URL = True

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
