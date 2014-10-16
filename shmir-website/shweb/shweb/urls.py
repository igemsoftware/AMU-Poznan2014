"""
.. module:: shweb.shweb
   :platform: Unix, Windows
   :synopsis: Main urls module (root) which contain url patterns

"""
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.views import generic

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'django.contrib.auth.views.login', name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name="logout"),
    url(r'^', include('designer.urls', namespace="designer")),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^about/$', generic.TemplateView.as_view(template_name="about.html"),
        name="about"),
)
