from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^item/page/info/(?P<item_id>[0-9a-z]+)/$', views.get_item_page_info, name='item-page-info'),
]
