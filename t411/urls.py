from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^api/', include('api.urls')),
    url(r'^announce', include('tracker.urls')),
    url(r'^scrape', include('tracker.urls_scrape')),
    url(r'^', include('home.urls'))
]
