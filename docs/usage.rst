Usage
-----
Add the app to installed apps::

    INSTALLED_APPS = (
        'django_nopassword',
    )

Set the authentication backend to *EmailBackend*::

    AUTHENTICATION_BACKENDS = ( 'django_nopassword.backends.EmailBackend', )

Add urls to your *urls.py*::

    urlpatterns = patterns('',
        url(r'^accounts/', include('django_nopassword.urls')),
    )


Post authenticate behavior
--------------------------

The method `post_authenticate_action` of the authentication backend is
called at the end of the authentication process. It's called with the
LoginCode instance as the only one argument. The default action is to
call `delete` on the login code.
