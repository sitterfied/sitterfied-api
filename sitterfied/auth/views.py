# -*- coding: utf-8 -*-
import logging

from django.contrib import auth
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from rest_framework import reverse, status

logger = logging.getLogger(__name__)


@sensitive_post_parameters()
@never_cache
@require_http_methods(['HEAD', 'POST'])
def login(request):
    if request.method == 'HEAD':
        # Force a new session cookie to be set if one is not present
        if not request.session.session_key:
            request.session.save()
            request.session.modified = True

        # Force the CSRF Middleware to set a new CSRF cookie on HEAD requests to
        # login so the front-end can use it to POST to login.
        request.META['CSRF_COOKIE_USED'] = True
        return HttpResponse()

    username = request.POST.get('username', None)
    password = request.POST.get('password', None)

    try:
        user = auth.authenticate(username=username, password=password)
    except:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(user, HttpResponse):
        return user

    if user is not None and user.is_active:
        auth.login(request, user)
        response = HttpResponse(status=status.HTTP_201_CREATED)
        response['Location'] = reverse.reverse('user-detail', args=[user.id], request=request)
        return response

    return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@sensitive_post_parameters()
@never_cache
@require_http_methods(['POST'])
def login_facebook(request):
    """
    Handle login using a Facebook session.

    """
    facebook_id = request.POST['id']

    user = auth.authenticate(id=facebook_id)
    if not user:
        request.session['FACEBOOK_ID'] = facebook_id
        request.session['FACEBOOK_TOKEN'] = request.POST.get('token', None)
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

    if user is not None and user.is_active:
        auth.login(request, user)
        response = HttpResponse(status=status.HTTP_201_CREATED)
        response['Location'] = reverse.reverse('user-detail', args=[user.id], request=request)
        return response

    return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
