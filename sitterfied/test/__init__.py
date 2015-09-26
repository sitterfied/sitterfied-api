# -*- coding: utf-8 -*-
import logging

from django.test.runner import DiscoverRunner
from rest_framework import renderers
from urllib.parse import urlencode


class APITestRunner(DiscoverRunner):
    """
    Custom test runner for the API. Turns off verbose logging by default.

    """
    def run_tests(self, *args, **kwargs):

        # Disable logging below a Critical level while testing
        logging.disable(logging.CRITICAL)

        return super(APITestRunner, self).run_tests(*args, **kwargs)


class FormRenderer(renderers.BaseRenderer):
    """
    This renderer allows us to send form data in tests.

    """
    media_type = 'application/x-www-form-urlencoded'
    format = 'form'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return urlencode(data)
