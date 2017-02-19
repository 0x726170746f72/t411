from django.conf.urls import url, include
from django.contrib import admin
from tracker import views

urlpatterns = [
    url(r'^$', views.scrape, name='scrape'),
]
