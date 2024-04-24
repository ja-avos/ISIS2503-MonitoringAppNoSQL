from django.conf.urls import url, include

from variables.views import *

urlpatterns = [
    url(r'^variables/$', variables),
    url(r'^variables/(?P<pk>\w+)/$', variablesDetail)
]