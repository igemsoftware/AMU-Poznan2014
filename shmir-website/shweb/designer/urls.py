from django.conf.urls import patterns, url

from designer.views import (
    DesignProcessCreateView,
    DesignProcessDetailView,
    DesignProcessHistoryView,
)


urlpatterns = patterns('',
    url(r"^$", DesignProcessCreateView.as_view(), name="create"),
    url(r"^history/", DesignProcessHistoryView.as_view(), name="history"),
    url(r"^(?P<process_id>[a-z0-9\-]{36})/$", DesignProcessDetailView.as_view(), name="detail"),
)
