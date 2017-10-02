from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^user/create', views.create_user),
    url(r'^user/get/(?P<user_id>[0-9]+)/$', views.get_user),
    url(r'^user/edit/(?P<user_id>[0-9]+)/$', views.edit_user),
    url(r'^user/delete/(?P<user_id>[0-9]+)/$', views.delete_user),
    url(r'^item/create', views.create_item),
    url(r'^item/get/(?P<item_id>[0-9]+)/$', views.get_item),
    url(r'^item/edit/(?P<item_id>[0-9]+)/$', views.edit_item),
    url(r'^item/delete/(?P<item_id>[0-9]+)/$', views.delete_item),
]
