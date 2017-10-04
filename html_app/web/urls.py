from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^item/display/(?P<item_id>[0-9a-z]+)/$', views.display_item, name='display-item'),
]
