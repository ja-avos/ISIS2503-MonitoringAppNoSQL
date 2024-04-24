from django.conf.urls import url
from .views import places, placeDetail, measurements, average

urlpatterns = [
    url(r'^places/$', places),
    url(r'^places/(?P<place_id>\w+)/$', placeDetail),
    url(r'^places/(?P<place_id>\w+)/measurements/$', measurements),
    url(r'^measurements/(?P<place_id>\w+)/$', measurements),
    url(r'^average/(?P<place_id>\w+)/$', average)
]