# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import FieldError

from django_nopassword.utils import User
from django_nopassword.models import LoginCode


class EmailBackend:

    supports_inactive_user = True

    def authenticate(self, code=None, **credentials):
        try:
            user = User.objects.get(**credentials)
            if not user.is_active:
                return None

            if code is None:
                return LoginCode.create_code_for_user(user)
            else:
                timestamp = datetime.now() - timedelta(seconds=getattr(settings, 'NOPASSWORD_LOGIN_CODE_TIMEOUT', 900))
                login_code = LoginCode.objects.get(user=user, code=code, timestamp__gt=timestamp)
                user = login_code.user
                user.code = login_code
                self.post_authenticate_action(login_code)
                return user
        except (TypeError, User.DoesNotExist, LoginCode.DoesNotExist, FieldError):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def post_authenticate_action(self, login_code):
        login_code.delete()
