# -*- coding: utf-8 -*-
from django.http import HttpResponse


def healthcheck(request):
    """
    Ping route for the ELB healthcheck.

    """
    return HttpResponse()
