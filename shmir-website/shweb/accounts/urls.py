"""
.. module:: shweb.accounts
   :platform: Unix, Windows
   :synopsis: Module with url patters for accounts application.

"""

from django.conf.urls import patterns, url

from accounts.views import (
    RegistrationView,
    AccountConfirmation,
)


urlpatterns = patterns('',
    url(r"^signup/$", RegistrationView.as_view(), name="signup"),
    url(r"^confirm/(?P<code>[A-Za-z0-9_\-]+)/$", AccountConfirmation.as_view(),
        name="confirm"),
    url(r"^password/reset/$", 'django.contrib.auth.views.password_reset',
        {'template_name': 'registration/password_reset_form.html',
         'post_reset_redirect': 'accounts:password_reset_done'}, name="password_reset"),
    url(r"^password/reset/done/$", 'accounts.views.password_reset_done',
        name="password_reset_done"),
    url(r"^password/reset/complete/$", 'accounts.views.password_reset_complete',
        name="password_reset_complete"),
    url(r"^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$",
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': 'accounts:password_reset_complete'},
        name="password_reset_confirm"),
)
