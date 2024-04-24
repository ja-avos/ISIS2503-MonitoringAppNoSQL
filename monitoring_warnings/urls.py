from django.conf.urls import url, include

from .views import *

urlpatterns = [
    url(r'^warnings/$', warnings),
    url(r'^warnings/(?P<pk>\w+)/$', warningDetail),
    url(r'^warningsFilter/$', warningsFilter),
]