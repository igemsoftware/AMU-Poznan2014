"""
.. module:: shweb.designer
   :platform: Unix, Windows
   :synopsis: Module with url patters for designer application.

"""
from django.conf.urls import patterns, url

from designer.views import (
    DesignProcessCreateView,
    DesignProcessSirnaCreateView,
    DesignProcessDetailView,
    DesignProcessHistoryView,
    DesignProcessNotifyView,
)


urlpatterns = patterns('',
    url(r"^$", DesignProcessCreateView.as_view(), name="create"),
    url(r"^sirna/$", DesignProcessSirnaCreateView.as_view(), name="create_sirna"),
    url(r"^history/", DesignProcessHistoryView.as_view(), name="history"),
    url(r"^(?P<process_id>[a-z0-9\-]{36})/$", DesignProcessDetailView.as_view(), name="detail"),
    url(r"^designer/notify_about_process_ending/(?P<process_id>[a-z0-9\-]{36})/$",
        DesignProcessNotifyView.as_view(), name="notify"),
)
