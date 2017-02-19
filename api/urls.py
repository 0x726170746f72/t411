from django.conf.urls import url, include
from django.contrib import admin
from api.api import T411
from api import views

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
#    url(r'^details/$', views.details, name='details'),
    url(r'^download/(?P<id>[0-9]+)/(?P<name>[^/]+)$', views.download, name='download')
]
