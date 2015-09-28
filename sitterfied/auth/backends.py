# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class BaseAuthBackend(object):
    """
    Base authentication backend class implements `get_user` method.

    """
    def authenticate(self, *args, **kwargs):
        raise NotImplementedError(
            '%s must implement the `authenticate` method.'
            % self.__class__.__name__
        )

    def get_user(self, user_id):
        """
        Get a User object from the user_id.

        """
        try:
            user = UserModel.objects.get(pk=user_id)
            if user.is_parent_or_sitter() is 'Parent':
                return user.parent
            elif user.is_parent_or_sitter() is 'Sitter':
                return user.sitter
            return user
        except UserModel.DoesNotExist:
            return None


class EmailAuthBackend(BaseAuthBackend):
    """
    Email Authentication Backend

    Allows a user to sign in using an email/password pair.

    """
    def authenticate(self, username=None, password=None):
        """
        Authenticate a user based on email address as the user name.

        """
        try:
            user = UserModel.objects.get(email__iexact=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None


class FacebookAuthBackend(BaseAuthBackend):
    """
    Facebook Authentication Backend

    Allows a user to sign in using a facebook token rather than
    a username/password pair.

    """
    def authenticate(self, id=None):
        try:
            return UserModel.objects.get(facebook_id=id)
        except UserModel.DoesNotExist:
            return None
