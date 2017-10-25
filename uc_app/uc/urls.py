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
    url(r'^item/get-by/(?P<field>[A-Za-z_]+)/(?P<criteria>[A-Za-z0-9]+)/$', views.get_item_by, name='get-item-by'),
    url(r'^item/edit/(?P<item_id>[0-9a-z]+)/$', views.edit_item, name='edit-item'),
    url(r'^item/delete/(?P<item_id>[0-9a-z]+)/$', views.delete_item, name='delete-item'),
    url(r'^user/login/$', views.log_in, name='login'),
    url(r'^user/logout/(?P<auth_id>[0-9a-z]+)/$', views.log_out, name='logout'),
    url(r'^auth/(?P<auth_id>[0-9a-z]+)/$', views.authenticate, name='auth'),
]
