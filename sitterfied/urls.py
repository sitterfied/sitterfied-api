# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from djrill import DjrillAdminSite
from rest_framework.routers import DefaultRouter

from sitterfied.app import api
from sitterfied.bookings.views import BookingViewSet
from sitterfied.children.views import ChildViewSet
from sitterfied.flows import views as flows_views
from sitterfied.healthcheck import views as healthcheck_views
from sitterfied.parents.views import ParentViewSet
from sitterfied.sitters.views import SitterViewSet
from sitterfied.users.views import UserViewSet

admin.site = DjrillAdminSite()
admin.autodiscover()

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)
router.register(r'certifications', api.CertificationViewSet)
router.register(r'children', ChildViewSet)
router.register(r'groups', api.GroupViewSet)
router.register(r'languages', api.LanguageViewSet)
router.register(r'otherservices', api.OtherServiceViewSet)
router.register(r'parents', ParentViewSet)
router.register(r'schedules', api.ScheduleViewSet)
router.register(r'settings', api.SettingsViewSet)
router.register(r'specialneeds', api.SpecialNeedViewSet)
router.register(r'sitters', SitterViewSet)
router.register(r'sitterreviews', api.ReviewViewSet)
router.register(r'users', UserViewSet)

# TODO: Remove the trailing slash from these endpoints
urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api/admin/', include(admin.site.urls)),
    url(r'^api/api-auth', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/flows/bookings/requests/', flows_views.booking_requests, name='flows-booking-requests'),
    url(r'^api/flows/bookings/tiers', flows_views.booking_tier, name='flows-booking-tier'),
    url(r'^api/search/$', 'sitterfied.app.views.search', name='search'),
    url(r'^api/__healthcheck', 'sitterfied.healthcheck.views.healthcheck', name='healthcheck'),
)

# TODO: Move this endpoint under the api, /api/sms
urlpatterns += patterns('',
    url(r'^sms/$', 'sitterfied.app.sms.sms_messages', name='sms_messages'),
)

# TODO: Refactor these endpoints in the front-end to use the actual resources
urlpatterns += patterns('',
    url(r'^login-ajax/$', 'sitterfied.auth.views.login', name='login'),
    url(r'^login-facebook/$', 'sitterfied.auth.views.login_facebook', name='login-facebook'),
    url(r'^onboarding/$', 'sitterfied.app.views.onboarding1', name='onboarding1'),
    url(r'^onboarding2/$', 'sitterfied.app.views.onboarding2', name='onboarding2'),
    url(r'^onboarding3/$', 'sitterfied.app.views.onboarding3', name='onboarding3'),
)
