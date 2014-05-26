# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import FieldError

from .utils import get_user_model
from .models import LoginCode


class EmailBackend:

    supports_inactive_user = True

    def authenticate(self, code=None, **credentials):
        try:
            user = get_user_model().objects.get(**credentials)
            if not user.is_active:
                return None

            if code is None:
                return LoginCode.create_code_for_user(user)
            else:
                timeout = getattr(settings, 'NOPASSWORD_LOGIN_CODE_TIMEOUT', 900)
                timestamp = datetime.now() - timedelta(seconds=timeout)
                login_code = LoginCode.objects.get(user=user, code=code, timestamp__gt=timestamp)
                user = login_code.user
                user.code = login_code
                self.post_authenticate_action(login_code)
                return user
        except (TypeError, get_user_model().DoesNotExist, LoginCode.DoesNotExist, FieldError):
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None

    def post_authenticate_action(self, login_code):
        login_code.delete()
