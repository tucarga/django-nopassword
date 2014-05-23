from django.contrib import admin

from .models import LoginCode


class LoginCodeAdmin(admin.ModelAdmin):

    list_display = ('user', 'code', 'next', 'timestamp')


admin.site.register(LoginCode, LoginCodeAdmin)
