# -*- coding: utf-8 -*-
import autofixture
import random

from django.contrib.auth.hashers import make_password
from django.test.testcases import TestCase
from hamcrest import assert_that, ends_with, has_entry, is_, not_none
from rest_framework import reverse, status

from sitterfied.test import random_string

url = '/login-ajax/'
facebook_url = '/login-facebook/'


class TestViews(TestCase):

    def setUp(self):
        self.account = autofixture.create_one('app.User', field_values={
            'email': 'user@test.sitterfied.com',
            'facebook_id': random.randint(0, 1000),
            'facebook_token': random_string(12),
            'username': 'user',
            'password': make_password('password'),
        })

    def test_get_csrftoken(self):
        response = self.client.head(url)
        assert_that(response.status_code, is_(status.HTTP_200_OK), str(response.content))
        assert_that(response.content, is_(''))
        assert_that(response.cookies, has_entry('csrftoken', not_none()))

    def test_login_failed(self):
        data = {
            'username': 'user@test.sitterfied.com',
            'password': '',
        }

        response = self.client.post(url, data, format='form')
        assert_that(response.status_code, is_(status.HTTP_401_UNAUTHORIZED), str(response.content))
        assert_that(response.content, is_(''))

    def test_login_success(self):
        data = {
            'username': 'user@test.sitterfied.com',
            'password': 'password',
        }

        response = self.client.post(url, data, format='form')
        assert_that(response.status_code, is_(status.HTTP_201_CREATED), str(response.content))
        assert_that(response.content, is_(''))
        assert_that(response['Location'], ends_with(reverse.reverse('user-detail', args=[self.account.id])))

    def test_login_with_facebook_failed(self):
        data = {
            'id': -1,
        }

        response = self.client.post(facebook_url, data, format='form')
        assert_that(response.status_code, is_(status.HTTP_401_UNAUTHORIZED), str(response.content))
        assert_that(response.content, is_(''))

    def test_login_with_facebook_success(self):
        data = {
            'id': self.account.facebook_id,
            'token': self.account.facebook_token,
        }

        response = self.client.post(facebook_url, data, format='form')
        assert_that(response.status_code, is_(status.HTTP_201_CREATED), str(response.content))
        assert_that(response.content, is_(''))
        assert_that(response['Location'], ends_with(reverse.reverse('user-detail', args=[self.account.id])))
