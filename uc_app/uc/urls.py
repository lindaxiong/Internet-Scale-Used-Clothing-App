from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^user/create/$', views.create_user, name='create-user'),
    url(r'^user/get/(?P<user_id>[0-9a-z]+)/$', views.get_user, name='get-user'),
    url(r'^user/edit/(?P<user_id>[0-9a-z]+)/$', views.edit_user, name='edit-user'),
    url(r'^user/delete/(?P<user_id>[0-9a-z]+)/$', views.delete_user, name='delete-user'),
    url(r'^item/create/$', views.create_item, name='create-item'),
    url(r'^item/get/(?P<item_id>[0-9a-z]+)/$', views.get_item, name='get-item'),
    url(r'^item/edit/(?P<item_id>[0-9a-z]+)/$', views.edit_item, name='edit-item'),
    url(r'^item/delete/(?P<item_id>[0-9a-z]+)/$', views.delete_item, name='delete-item'),
]
